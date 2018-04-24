# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests.common import TransactionCase


class TestHrAttendance(TransactionCase):

    def setUp(self):
        super(TestHrAttendance, self).setUp()
        self.employee_model = self.env['hr.employee']
        self.test_employee = self.browse_ref('hr.employee_al')
        self.rfid_card_code = '5b3f5'
        self.test_employee.rfid_card_code = self.rfid_card_code

    def test_valid_employee(self):
        res = self.employee_model.register_rfid_attendance_event(
            self.rfid_card_code)
        self.assertTrue('action' in res and res['action'] == 'check_in')
        self.assertTrue('logged' in res and res['logged'])
        self.assertTrue(
            'rfid_card_code' in res and
            res['rfid_card_code'] == self.rfid_card_code)

        logs = self.env['hr.employee.rfid.access.log'].search(
            [('rfid_card_code', '=', self.rfid_card_code)])
        self.assertEqual(len(logs), 2)
        res = self.employee_model.register_rfid_attendance_event(
            self.rfid_card_code)
        self.assertTrue('action' in res and res['action'] == 'check_out')
        self.assertTrue('logged' in res and res['logged'])
        logs = self.env['hr.employee.rfid.access.log'].search(
            [('rfid_card_code', '=', self.rfid_card_code)])
        self.assertEqual(len(logs), 4)

    def test_invalid_code(self):
        invalid_code = '029238d'
        res = self.employee_model.register_rfid_attendance_event(invalid_code)
        self.assertTrue('action' in res and not res['action'])
        self.assertTrue('logged' in res and not res['logged'])
        self.assertTrue(
            'rfid_card_code' in res and
            res['rfid_card_code'] == invalid_code)
        logs = self.env['hr.employee.rfid.access.log'].search(
            [('rfid_card_code', '=', invalid_code)])
        self.assertEqual(len(logs), 1)
