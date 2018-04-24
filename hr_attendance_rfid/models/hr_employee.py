# -*- coding: utf-8 -*-
# Copyright 2017 Comunitea Servicios Tecnológicos S.L.
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models, fields, _


class HrEmployee(models.Model):

    _inherit = "hr.employee"

    rfid_card_code = fields.Char("RFID Card Code")

    @api.model
    def _log_rfid_access(self, employee=None, card_code=False, message=''):
        self.env['hr.employee.rfid.access.log'].create({
            'description': message,
            'employee_id': employee and employee.id or False,
            'rfid_card_code': card_code,
        })

    @api.model
    def register_attendance(self, card_code):
        """ Register the attendance of the employee.
        :returns: dictionary
            'rfid_card_code'
            'employee_name'
            'employee_id'
            'error_message'
            'logged'
            'action'
        """

        res = {
            'rfid_card_code': card_code,
            'employee_name': '',
            'employee_id': False,
            'error_message': '',
            'logged': False,
            'action': '',
        }
        employee = self.search([('rfid_card_code', '=', card_code)], limit=1)        
        if employee:
            res['employee_name'] = employee.name
            res['employee_id'] = employee.name
            msg = _("%s logged with card %s") % (employee.name, card_code)
            self._log_rfid_access(employee=employee, card_code=card_code, 
                                  message=msg)
        else:
            msg = _("No employee found with card %s") % card_code
            self._log_rfid_access(employee=employee, card_code=card_code, 
                                  message=msg)
            res['error_message'] = msg            
            return res
        try:
            attendance = employee.attendance_action_change()
            if attendance:
                msg = _('Attendance recorded for employee %s') % employee.name                
                self._log_rfid_access(employee=employee, card_code=card_code,
                                      message=msg)                
                res['logged'] = True
                if attendance.check_out:
                    res['action'] = 'check_out'
                else:
                    res['action'] = 'check_in'
                return res
            else:
                msg = _('No attendance was recorded for '
                        'employee %s') % employee.name                
                self._log_rfid_access(employee=employee, card_code=card_code,
                                      message=msg)
                res['error_message'] = msg
                return res
        except Exception as e:
            msg = e.message
            self._log_rfid_access(employee=employee, card_code=card_code,
                                  message=msg)
            res['error_message'] = msg            
        return res
