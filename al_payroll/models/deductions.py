# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import time
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class HrDeductions(models.Model):
    _name = "hr.deductions"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "HR Deductions"

    name = fields.Char(string='Description', required=True, states={'draft': [('readonly', False)]})
    date = fields.Date(string="Date", readonly=True, states={'draft': [('readonly', False)]}, default=fields.Date.context_today)
    deduction_date = fields.Date(string='Deduction Day', required=True, states={'draft': [('readonly', False)]})
    manager_id = fields.Many2one(related='employee_id.parent_id', string="Manager", required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    department_id = fields.Many2one(related='employee_id.department_id', string="Department", store=True)
    coach_id = fields.Many2one(related='employee_id.coach_id', string="Coach", store=True)
    rule_id = fields.Many2one('hr.salary.rule', string='Salary Rule')
    job_id = fields.Many2one(related='employee_id.job_id', string="Job Position", store=True)
    unit_amount = fields.Float("Unit Price", required=True, states={'draft': [('readonly', False)]})
    quantity = fields.Float(string="Quantity", states={'draft': [('readonly', False)]}, default=1)
    total_amount = fields.Float(string="Total", compute='_compute_amount', store=True)
    description = fields.Text('Notes...', states={'draft': [('readonly', False)], 'refused': [('readonly', False)]})
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('approve', 'Approved'),
        ('refused', 'Refused')
    ], string='Status', default='draft')
    reference = fields.Char("Reference", required=False)

    @api.model
    def _default_manager_id(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    @api.depends('quantity', 'unit_amount')
    def _compute_amount(self):
        for amount in self:
            amount.total_amount = amount.unit_amount * amount.quantity

    @api.multi
    def action_deductions_draft(self):
        return self.write({'state': 'draft'})

    @api.multi
    def action_deductions_submit(self):
        return self.write({'state': 'submit'})


    @api.multi
    def action_deductions_approve(self):
        return self.write({'state': 'approve'})


    @api.multi
    def action_deductions_refused(self):
        return self.write({'state': 'refused'})


