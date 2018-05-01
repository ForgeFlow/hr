import json

from odoo import http


class MQTTController(http.Controller):

    @http.route('/mqtt-broker-config/<string:mqtt_id>',
        type='http', method='GET', auth="user")
    def mqtt_broker_config(self, mqtt_id, **kwargs):
        """ Look that ID given is in system.
         :return json with new configuration
         """
        values = self._prepare_config_broker(mqtt_id)
        return json.dumps(values)

    def _prepare_config_broker(self, broker_id):
        broker = self.env['mqtt_broker'].search([
            (broker_id, 'in', self.mqtt_broker_id)])
        res = 'message:Mock MQTT broker config'
        return res

    @http.route('/mqtt-client-config/<string:mqtt_client_id>',
                type='http', method='GET', auth="user")
    def mqtt_broker_config(self, mqtt_client_id):
        """ Look that ID given is in system.
         :return json with new configuration
         """
        values = self._prepare_config_client(mqtt_client_id)
        return json.dumps(values)

    def _prepare_config_client (self, client_id):
        broker = self.env['mqtt_client'].search([
            (client_id, 'in', self.client_id)])
        res = 'message:Mock MQTT client config'
        return res
