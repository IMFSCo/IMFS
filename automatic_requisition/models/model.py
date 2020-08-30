from odoo import models, fields, api,_
from datetime import date, datetime
from odoo.exceptions import ValidationError

class InheritManufacturing(models.Model):
    _inherit = 'mrp.production'
    has_requisition = fields.Boolean(default=False)
    requisition_count = fields.Integer(compute='_requisition_count')

    def create_requisition(self):
        if self.has_requisition == True:
            raise ValidationError(_('Requisition Already Created for this document.'))
        rec = []
        for items in self.move_raw_ids:
            rec.append((0, 0, {'product_id': items.product_id.id,
                               'description': items.product_id.name,
                               'qty': items.product_uom_qty,
                               'uom':items.product_id.uom_id.id}))
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        self.env['internal.requisition'].create({'request_emp':employee.id,
                                                 'department_id':employee.department_id.id,
                                                 'desti_loca_id':employee.desti_loca_id.id,
                                                 'fixed_asset_desti_loca_id':employee.fixed_asset_desti_loca_id.id,
                                                 'request_date':date.today(),
                                                 'date_end':datetime.now(),
                                                 'mo_reference':self.name,
                                                 'requisition_line_ids': rec})
        self.has_requisition = True


    def requisition_view(self):
        req_ids = []
        for obj in self:
            req_obj = self.env['internal.requisition'].sudo().search([])
            requisition_id = req_obj.filtered(
                lambda x: x.mo_reference == self.name)
            for item in requisition_id:
                req_ids.append(item.id)
            view_id = self.env.ref('material_internal_requisitions.material_internal_requisition_form_view').id
            if req_ids:
                value = {
                        'view_type': 'form',
                        'view_mode': 'form',
                        'res_model': 'internal.requisition',
                        'view_id': view_id,
                        'type': 'ir.actions.act_window',
                        'name': _('Internal Requisition'),
                        'res_id': req_ids and req_ids[0]
                    }
                return value

    @api.multi
    def _requisition_count(self):
        for obj in self:
            requisition_ids = self.env['internal.requisition'].sudo().search([])
            requisition = requisition_ids.filtered(lambda x: x.mo_reference == self.name)
            print(requisition)
        obj.requisition_count = len(requisition)


