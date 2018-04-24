# -*- coding: utf-8 -*-
# Copyright 2017 Comunitea Servicios Tecnológicos S.L.
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models, fields


class HrEmployeeRfidAccessLog(models.Model):

    _name = "hr.employee.rfid.access.log"
    _rec_name = "description"

    description = fields.Char("Message", required=True)
    employee_id = fields.Many2one("hr.employee", "Employee")
    rfid_card_code = fields.Char("RFID Card Code", required=True)
    create_date = fields.Datetime("Create date", readonly=True)
