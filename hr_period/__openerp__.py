# -*- coding:utf-8 -*-
# Copyright 2015 Savoir-faire Linux. All Rights Reserved.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Payroll Period',
    'version': '9.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Generic Modules/Human Resources',
    'summary': "Add payroll periods",
    'author': "Savoir-faire Linux, "
              "Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/hr',
    'depends': [
        'hr_payroll',
    ],
    'data': [
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/hr_period_view.xml',
        'views/hr_fiscalyear_view.xml',
        'views/hr_payslip_view.xml',
        'views/hr_payslip_run_view.xml',
        'views/hr_payslip_employee_view.xml',
    ],
    'installable': True,
}