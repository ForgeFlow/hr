from odoo import api, models, fields, _

"""
This models aim to generate and API response to be auto-configurable.
Notice that this kind of configuration maybe has to be done via custom
script.
"""

class MQTTClient(models.Model):
    """
    This model allow to identify RFID by his ID assigning parameters to
    be autodiscovered.

    """
    _name = 'mqtt_client'

    mqtt_name = fields.Char(string="rfid name")
    mqtt_client_id = fields.One2many(string='RFID ID', required=True, default='None')
    mqtt_broker_id = fields.Many2one('mqtt_attendance_broker',
                                     string='MQTT Server ID',
                                     required=True, default='None')
    hmac = fields.Char(string="HMAC", size=16)

    state = fields.Selection([
        ('enable', "Enable"),
        ('config', "Configuration"),
        ('disable', "Disable"),
        ('error', "Error"),
        ('waiting', "Waiting"),
        ])
    mqtt_client_user = fields.Char(string = "MQTT client user")
    mqtt_client_password = fields.Char(string="MQTT client password")


class MQTTBroker(models.Models):
    """
    This Model allow to identify MQTT broker assigning parameters to his correct
    configuration
    """
    _name = 'mqtt_broker'

    mqtt_broker_id = fields.One2many(string='MQTT Server ID', required=True,
                                     default='None')
    rfid_ids = fields.Many2many('mqtt_attendance_broker', string='')
    url = fields.Char(String='MQTT Server URL')
    state = fields.Selection([
        ('online', "Online"),
        ('config', "Configuration"),
        ('offline', "Done"),
        ])

