# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class TestBusModel(models.Model):
    _name = 'test.bus.model'
    _description = 'Test Bus Model'
    
    name = fields.Char()
    counter = fields.Integer(default=0)
    
    def action_trigger_bus(self):
        """Send bus notification"""
        self.ensure_one()
        self.counter += 1
        
        self.env['bus.bus']._sendone(
            'test_bus_channel',
            'test_notification',
            { 
                'counter': self.counter,
                'message': f'Counter is now {self.counter}',
                'model': 'test.bus.model',
                'id': self.id,
            }
        )
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Bus Notification Sent',
                'message': f'Check browser console for message!',
                'type': 'success',
                'sticky': False,
            }
        }