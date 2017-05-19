# -*- coding:utf-8 -*-
# Copyright 2015 Savoir-faire Linux. All Rights Reserved.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    hr_period_id = fields.Many2one(
        'hr.period',
        string='Period',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    date_payment = fields.Date(
        'Date of Payment',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )

    @api.multi
    @api.constrains('hr_period_id', 'company_id')
    def _check_period_company(self):
        for slip in self:
            if slip.hr_period_id:
                if slip.hr_period_id.company_id != slip.company_id:
                    raise UserError("The company on the selected period must "
                                    "be the same as the company on the "
                                    "payslip.")

    @api.onchange('company_id', 'contract_id')
    def onchange_company_id(self):
        if self.company_id and self.contract_id:
            contract = self.contract_id
            period_obj = self.env['hr.period']
            period = period_obj.get_next_period(self.company_id.id,
                                                contract.schedule_pay)
            self.hr_period_id = period.id if period else False

    @api.multi
    def onchange_contract_id(self, date_from, date_to,
                             employee_id=False, contract_id=False):
        res = super(HrPayslip, self).onchange_contract_id(
            date_from, date_to,
            employee_id=employee_id, contract_id=contract_id)

        if employee_id and contract_id:
            employee = self.env['hr.employee'].browse(employee_id)
            contract = self.env['hr.contract'].browse(contract_id)

            period = self.env['hr.period'].get_next_period(
                employee.company_id.id, contract.schedule_pay)
            if period:
                res['value'].update({
                    'hr_period_id': period.id if period else False,
                    'name': _('Salary Slip of %s for %s') % (
                        employee.name, period.name),
                })
        return res

    @api.onchange('hr_period_id')
    def onchange_hr_period_id(self):
        if self.hr_period_id:
            period = self.hr_period_id
            self.date_from = period.date_start
            self.date_to = period.date_stop
            self.date_payment = period.date_payment

    @api.model
    def create(self, vals):
        if vals.get('payslip_run_id'):
            payslip_run = self.env['hr.payslip.run'].browse(
                vals['payslip_run_id'])

            employee = self.env['hr.employee'].browse(vals['employee_id'])
            period = payslip_run.hr_period_id

            vals['date_payment'] = payslip_run.date_payment
            vals['hr_period_id'] = period.id
            vals['name'] = _('Salary Slip of %s for %s') % (
                employee.name, period.name)

        elif vals.get('date_to') and not vals.get('date_payment'):
            vals['date_payment'] = vals['date_to']

        return super(HrPayslip, self).create(vals)