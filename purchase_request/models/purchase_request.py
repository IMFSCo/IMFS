# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo import api, fields, models, _
import datetime
from odoo.exceptions import UserError
from odoo.exceptions import UserError, AccessError, ValidationError
import odoo.addons.decimal_precision as dp

_STATES = [
    ('draft', 'Draft'),
    ('to_approve', 'To be approved'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('done', 'Done')
]



class PurchaseRequest(models.Model):

    _name = 'purchase.request'
    _description = 'Purchase Request'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    @api.model
    def _company_get(self):
        company_id = self.env['res.company']._company_default_get(self._name)
        return self.env['res.company'].browse(company_id.id)

    @api.model
    def _get_default_requested_by(self):
        return self.env['res.users'].browse(self.env.uid)

    @api.model
    def _get_default_name(self):
        return self.env['ir.sequence'].next_by_code('purchase.request')


    @api.model
    def _default_picking_type(self):
        type_obj = self.env['stock.picking.type']
        company_id = self.env.context.get('company_id') or \
            self.env.user.company_id.id
        types = type_obj.search([('code', '=', 'incoming'),
                                 ('warehouse_id.company_id', '=', company_id)])
        if not types:
            types = type_obj.search([('code', '=', 'incoming'),
                                     ('warehouse_id', '=', False)])
        return types[:1]

    @api.multi
    @api.depends('state')
    def _compute_is_editable(self):
        for rec in self:
            if rec.state in ('to_approve', 'approved', 'rejected', 'done'):
                rec.is_editable = False
            else:
                rec.is_editable = True

    @api.multi
    def _track_subtype(self, init_values):
        for rec in self:
            if 'state' in init_values and rec.state == 'to_approve':
                return 'purchase_request.mt_request_to_approve'
            elif 'state' in init_values and rec.state == 'approved':
                return 'purchase_request.mt_request_approved'
            elif 'state' in init_values and rec.state == 'rejected':
                return 'purchase_request.mt_request_rejected'
            elif 'state' in init_values and rec.state == 'done':
                return 'purchase_request.mt_request_done'
        return super(PurchaseRequest, self)._track_subtype(init_values)

    name = fields.Char('Request Reference', size=32, required=True,
                       default=_get_default_name,
                       track_visibility='onchange')
    origin = fields.Char('Source Document', size=32)
    date_start = fields.Date('Creation date',
                             help="Date when the user initiated the "
                                  "request.",
                             default=fields.Date.context_today,
                             track_visibility='onchange')
    requested_by = fields.Many2one('res.users',
                                   'Requested by',
                                   required=True,
                                   track_visibility='onchange',
                                   default=_get_default_requested_by)
    assigned_to = fields.Many2one('res.users', 'Approver',
                                  track_visibility='onchange')
    description = fields.Text('Description')
    company_id = fields.Many2one('res.company', 'Company',
                                 required=True,
                                 default=_company_get,
                                 track_visibility='onchange')
    line_ids = fields.One2many('purchase.request.line', 'request_id',
                               'Products to Purchase',
                               copy=True,
                               track_visibility='onchange')
    # state = fields.Selection(selection=_STATES,
    #                          string='Status',
    #                          index=True,
    #                          track_visibility='onchange',
    #                          required=True,
    #                          copy=False,
    #                          default='draft')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit','Submitted'),
        ('to_approve', 'To Approve'),
        ('approval1','DPD-OP Approval'),
        ('approval2','FD Approval'),
        ('approval3','PD Approval'),
        ('approved', 'Approved'),
        ('rejected','Rejected'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
    

    is_editable = fields.Boolean(string="Is editable",
                                 compute="_compute_is_editable")
    to_approve_allowed = fields.Boolean(
        compute='_compute_to_approve_allowed')
    picking_type_id = fields.Many2one('stock.picking.type',
                                      'Picking Type', required=True,
                                      default=_default_picking_type)

    reject_reason = fields.Text(string="Reject Reason",track_visibility='always')
    
    submit_email = fields.Char()
    first_email = fields.Char()
    second_email = fields.Char()
    third_email = fields.Char()

    line_count = fields.Integer(
        string='Purchase Request Line count',
        compute='_compute_line_count',
    )

    @api.multi
    def button_change_state_to_rejected(self):
      for order in self:
        if order.state not in ['submit','approved','approval1','approval2','approval3','approval4']:
            continue
        else:
          if not order.reject_reason:
            raise ValidationError('Add Reject Reason')

          else:
            if self.state == 'submit':
              emails = self.submit_email
            if self.state == 'approval1':
              emails = self.submit_email,self.first_email
            if self.state == 'approval2':
              emails = self.submit_email,self.first_email,self.second_email
            if self.state == 'approval3':
              emails = self.submit_email,self.first_email,self.second_email,self.third_email

            template_id = self.env.ref('purchase_request.email_template_purchase_order_reject').id
            template = self.env['mail.template'].browse(template_id)
            template.write({'email_to': emails})
            template.send_mail(self.id,force_send=True)
            self.write({'reject_reason':'','state':'rejected','submit_email':'','first_email':'','second_email':'','third_email':'','fourth_email':''})



    @api.multi
    def submit_purchase_request(self):
        return self.write({'state':'submit','submit_email':self.env.user.email_formatted})

    @api.multi
    def button_approval_one(self):
        return self.write({'state':'approval1','first_email':self.env.user.email_formatted})

    @api.multi
    def button_approval_two(self):
        return self.write({'state':'approval2','second_email':self.env.user.email_formatted})

    @api.multi
    def button_approval_three(self):
        return self.write({'state':'approval3','third_email':self.env.user.email_formatted})

    @api.depends('line_ids')
    def _compute_line_count(self):
        self.line_count = len(self.mapped('line_ids'))

    @api.multi
    def action_view_purchase_request_line(self):
        action = self.env.ref(
            'purchase_request.purchase_request_line_form_action').read()[0]
        lines = self.mapped('line_ids')
        if len(lines) > 1:
            action['domain'] = [('id', 'in', lines.ids)]
        elif lines:
            action['views'] = [(self.env.ref(
                'purchase_request.purchase_request_line_form').id, 'form')]
            action['res_id'] = lines.id
        return action

    @api.multi
    @api.depends(
        'state',
        'line_ids.product_qty',
        'line_ids.cancelled',
    )
    def _compute_to_approve_allowed(self):
        for rec in self:
            rec.to_approve_allowed = (
                rec.state in ('draft','submit') and
                any([
                    not line.cancelled and line.product_qty
                    for line in rec.line_ids
                ])
            )

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        self.ensure_one()
        default.update({
            'state': 'draft',
            'name': self.env['ir.sequence'].next_by_code('purchase.request'),
        })
        return super(PurchaseRequest, self).copy(default)


    @api.multi
    def button_draft(self):
        self.mapped('line_ids').do_uncancel()
        return self.write({'state': 'draft'})

    @api.multi
    def button_to_approve(self):
        self.to_approve_allowed_check()
        return self.write({'state': 'to_approve'})

    @api.multi
    def button_approved(self):
        return self.write({'state': 'approved'})

    @api.multi
    def button_rejected(self):
        self.mapped('line_ids').do_cancel()
        return self.write({'state': 'rejected'})

    @api.multi
    def button_done(self):
        return self.write({'state': 'done'})

    @api.multi
    def check_auto_reject(self):
        """When all lines are cancelled the purchase request should be
        auto-rejected."""
        for pr in self:
            if not pr.line_ids.filtered(lambda l: l.cancelled is False):
                pr.write({'state': 'rejected'})

    @api.multi
    def to_approve_allowed_check(self):
      for rec in self:
        if not rec.to_approve_allowed:
          raise UserError(
              _("You can't request an approval for a purchase request "
                      "which is empty. (%s)") % rec.name)


class PurchaseRequestLine(models.Model):

    _name = "purchase.request.line"
    _description = "Purchase Request Line"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    
    @api.multi
    @api.depends('product_id', 'name', 'product_uom_id', 'product_qty',
                 'analytic_account_id', 'date_required', 'specifications')
    def _compute_is_editable(self):
        for rec in self:
            if rec.request_id.state in ('to_approve', 'approved', 'rejected',
                                        'done'):
                rec.is_editable = False
            else:
                rec.is_editable = True

    @api.multi
    def _compute_supplier_id(self):
        for rec in self:
            rec.supplier_id = self.env['res.partner'].search([('name', 'ilike', 'INTERNATIONAL MEDICAL FURNITURE & SUPPLIES')])


    product_id = fields.Many2one(
        'product.product', 'Product',
        domain=[('purchase_ok', '=', True)],
        track_visibility='onchange')
    name = fields.Char('Description', size=256,
                       track_visibility='onchange')
    product_uom_id = fields.Many2one('product.uom', 'Product Unit of Measure',
                                     track_visibility='onchange')
    product_qty = fields.Float('Quantity', track_visibility='onchange',
                               digits=dp.get_precision(
                                   'Product Unit of Measure'))
    request_id = fields.Many2one('purchase.request',
                                 'Purchase Request',
                                 ondelete='cascade')
    company_id = fields.Many2one('res.company',
                                 related='request_id.company_id',
                                 string='Company',
                                 store=True)
    analytic_account_id = fields.Many2one('account.analytic.account',
                                          'Analytic Account',
                                          track_visibility='onchange')
    requested_by = fields.Many2one('res.users',
                                   related='request_id.requested_by',
                                   string='Requested by',
                                   store=True)
    assigned_to = fields.Many2one('res.users',
                                  related='request_id.assigned_to',
                                  string='Assigned to',
                                  store=True)
    date_start = fields.Date(related='request_id.date_start',
                             string='Request Date',store=True)
    description = fields.Text(related='request_id.description',
                              string='Description',store=True)
    origin = fields.Char(related='request_id.origin',
                         size=32, string='Source Document',
                         store=True)
    date_required = fields.Datetime(string='Request Date', required=True,
                                track_visibility='onchange',
                                default=datetime.datetime.today())
    is_editable = fields.Boolean(string='Is editable',
                                 compute="_compute_is_editable",
                                 )
    specifications = fields.Text(string='Specifications')
    request_state = fields.Selection(string='Request state',
                                     related='request_id.state',
                                     selection=_STATES,
                                     store=True)
    state = fields.Selection([
            ('draft', 'Draft'),('sent', 'Sent'),('confirmed', 'Confirmed'),('cancelled', 'Cancelled')  
        ], string='Status', default='draft', readonly=True, required=True, copy=False,
        help="If event is created, the status is 'Draft'. If event is confirmed for the particular dates the status is set to 'Confirmed'. If the event is over, the status is set to 'Done'. If event is cancelled the status is set to 'Cancelled'.")

    supplier_id = fields.Many2one('res.partner',
                                  string='Preferred supplier',
                                  compute="_compute_supplier_id")
    
    cancelled = fields.Boolean(
        string="Cancelled",default=False, copy=False)

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            name = self.product_id.name
            if self.product_id.code:
                name = '[%s] %s' % (name, self.product_id.code)
            if self.product_id.description_purchase:
                name += '\n' + self.product_id.description_purchase
            self.product_uom_id = self.product_id.uom_id.id
            self.product_qty = 1
            self.name = name

    @api.multi
    def do_cancel(self):
        """Actions to perform when cancelling a purchase request line."""
        self.write({'cancelled': True})

    @api.multi
    def do_uncancel(self):
        """Actions to perform when uncancelling a purchase request line."""
        self.write({'cancelled': False})

    @api.multi
    def write(self, vals):
        res = super(PurchaseRequestLine, self).write(vals)
        if vals.get('cancelled'):
            requests = self.mapped('request_id')
            requests.check_auto_reject()
        return res

class InheritPurchase(models.Model):
    _inherit = 'purchase.order'

    is_quantity_copy = fields.Selection([('draft', 'RFQ'),
        ('sent', 'RFQ Sent')],string="is quantity", readonly=True)
    is_req_for_purchase = fields.Boolean(default=False)
    purchase_req_reference = fields.Char()
    reject_reason = fields.Text(string="Reject Reason",track_visibility='always')
    
    submit_email = fields.Char()
    first_email = fields.Char()
    second_email = fields.Char()
    third_email = fields.Char()
    fourth_email = fields.Char()

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('submit','Submitted'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('approval1','PM Approval'),
        ('approval2','DPD-OP Approval'),
        ('approval3','FD Approval'),
        ('approval4','PD Approval'),
        ('reject','Rejected'),
        ('done', 'Confirm'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
    

    @api.multi
    def button_confirm(self):
      self.ensure_one()
      ir_model_data = self.env['ir.model.data']
      for order in self:
        if order.state not in ['draft', 'sent','approval4']:
            continue
        order._add_supplier_to_product()
        # Deal with double validation process
        if order.company_id.po_double_validation == 'one_step' \
                or (order.company_id.po_double_validation == 'two_step' \
                    and order.amount_total < self.env.user.company_id.currency_id._convert(
                    order.company_id.po_double_validation_amount, order.currency_id, order.company_id,
                    order.date_order or fields.Date.today())) \
                or order.user_has_groups('purchase.group_purchase_manager'):
            order.button_approve()
        else:
            order.write({'state': 'to approve'})
      self.write({'state':'done'})
      
      try:  
        template_id = ir_model_data.get_object_reference('purchase_request', 'email_template_purchase_order_confirm')[1]
      except ValueError:
        template_id = False
      try:
          compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
      except ValueError:
          compose_form_id = False
      ctx = dict(self.env.context or {})
      ctx.update({
          'default_model': 'purchase.order',
          'default_res_id': self.ids[0],
          'default_use_template': bool(template_id),
          'default_template_id': template_id,
          'default_composition_mode': 'comment',
          'custom_layout': "mail.mail_notification_paynow",
          'force_email': True,
          'mark_rfq_as_sent': True,
      })

      # In the case of a RFQ or a PO, we want the "View..." button in line with the state of the
      # object. Therefore, we pass the model description in the context, in the language in which
      # the template is rendered.
      lang = self.env.context.get('lang')
      if {'default_template_id', 'default_model', 'default_res_id'} <= ctx.keys():
          template = self.env['mail.template'].browse(ctx['default_template_id'])
          if template and template.lang:
              lang = template.render_template(template.lang, ctx['default_model'], ctx['default_res_id'])

      self = self.with_context(lang=lang)
      ctx['model_description'] = _('Request for Purchase')
      
      return {
          'name': _('Compose Email'),
          'type': 'ir.actions.act_window',
          'view_type': 'form',
          'view_mode': 'form',
          'res_model': 'mail.compose.message',
          'views': [(compose_form_id, 'form')],
          'view_id': compose_form_id,
          'target': 'new',
          'context': ctx,
      }
        
    @api.multi
    def button_confirm_old(self):
        for order in self:
            if order.state not in ['draft', 'sent','approval4']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step'\
                    or (order.company_id.po_double_validation == 'two_step'\
                        and order.amount_total < self.env.user.company_id.currency_id._convert(
                            order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
        return True

    @api.multi
    def submit_quotation(self):
        return self.write({'state':'submit','submit_email':self.env.user.email_formatted})

    @api.multi
    def button_approval_one(self):
        return self.write({'state':'approval1','first_email':self.create_uid.email_formatted})

    @api.multi
    def button_approval_two(self):
        return self.write({'state':'approval2','second_email':self.create_uid.email_formatted})

    @api.multi
    def button_approval_three(self):
        return self.write({'state':'approval3','third_email':self.create_uid.email_formatted})

    @api.multi
    def button_approval_four(self):
        return self.write({'state':'approval4','fourth_email':self.create_uid.email_formatted})

    @api.multi
    def button_change_state_to_confirm(self):
        self.name = self.env['ir.sequence'].next_by_code('purchase.order')
        self.write({'state': 'purchase'})

    @api.multi
    def button_change_state_to_rejected(self):
      for order in self:
        if order.state not in ['submit','purchase','approval1','approval2','approval3','approval4']:
            continue
        else:
          if not order.reject_reason:
            raise ValidationError('Add Reject Reason')

          else:
            if self.state == 'submit':
              emails = self.submit_email
            if self.state == 'approval1':
              emails = self.submit_email,self.first_email
            if self.state == 'approval2':
              emails = self.submit_email,self.first_email,self.second_email
            if self.state == 'approval3':
              emails = self.submit_email,self.first_email,self.second_email,self.third_email
            if self.state == 'approval4':
              emails = self.submit_email,self.first_email,self.second_email,self.third_email,self.fourth_email

            template_id = self.env.ref('purchase_request.email_template_purchase_order_reject').id
            template = self.env['mail.template'].browse(template_id)
            template.write({'email_to': emails})
            template.send_mail(self.id,force_send=True)
            self.write({'reject_reason':'','state':'reject','first_email':'','second_email':'','third_email':'','fourth_email':''})

    @api.multi
    def button_change_state_to_draft(self):
      for order in self:
        if order.state not in ['reject']:
            continue
        else:
          self.write({'state':'draft','first_email':'','second_email':'','third_email':'','fourth_email':''})


class InheritEmail(models.TransientModel):
    _inherit = 'mail.compose.message'

    def create_rfqs(self):
        reference = self.subject.split(' ')
        po_obj = self.env['purchase.order'].search([('name','=',reference[1])])
        for rec in self.partner_ids:
            po = self.env['purchase.order'].create({'id':self.id,
                                               'name':self.env['ir.sequence'].next_by_code('request.for.quotation'),
                                               'partner_id':rec.id,
                                               'purchase_req_reference':reference[1],
                                               'is_req_for_purchase':True})
            for lines in po_obj.order_line:

                po.order_line.create({'order_id':po.id,
                                      'product_id':lines.product_id.id,
                                      'name':lines.name,
                                      'product_qty':lines.product_qty,
                                      'price_unit':0.0,
                                      'product_uom': lines.product_uom.id,
                                      'date_planned':datetime.datetime.now()})


    @api.multi
    def send_mail(self, auto_commit=False):
        self.create_rfqs()
        res = super(InheritEmail, self).send_mail()
        return res

class RejectReason(models.TransientModel):
    _name = 'request.reject'
    reason_for_rejection = fields.Text(string='Reason')

    def submit_reason(self):
        rec = self.env['purchase.request'].search([('id', '=', self._context['active_id'])])
        rec.reject_reason = self.reason_for_rejection
        rec.button_change_state_to_rejected()

class RequestPurchaseRejectReason(models.TransientModel):
    _name = 'request.purchase.reason'
    reason_for_rejection = fields.Text(string='Reason')

    def submit_reason(self):
        rec = self.env['purchase.order'].search([('id', '=', self._context['active_id'])])
        rec.reject_reason = self.reason_for_rejection
        rec.button_change_state_to_rejected()



class InheritPurchaseReport(models.Model):
    _inherit = 'purchase.report'

    # product_qty = fields.Float(string='Quote', digits=dp.get_precision('Product Unit of Measure'), readonly=True)
    v_desc = fields.Char('Description', readonly=True)
    pr_reference = fields.Char('PR Reference', readonly=True)

    def _select(self):
      return super(InheritPurchaseReport, self)._select() + ", s.notes as v_desc,s.purchase_req_reference as pr_reference"

    def _group_by(self):
      return super(InheritPurchaseReport, self)._group_by() + ", s.notes,s.purchase_req_reference"


    
