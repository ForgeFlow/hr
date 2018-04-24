# -*- coding: utf-8 -*-
# Copyright 2017 Comunitea Servicios Tecnológicos S.L.
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'HR Attendance RFID',
    'version': '10.0.1.0.0',
    'category': 'Human Resources',
    'website': 'https://github.com/OCA/hr',
    'author': 'Comunitea,'
              'Eficent,'
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'hr_attendance',
    ],
    'data': ['security/ir.model.access.csv',
             'views/hr_employee_rfid_access_log_view.xml',
             'views/hr_employee_view.xml'],
}
