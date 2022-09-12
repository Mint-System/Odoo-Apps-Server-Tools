from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import ValidationError
import datetime


class Metric(models.Model):
    _name = 'ir.metric'
    _description = 'Metrics'

    name = fields.Char(required=True)
    description = fields.Char()
    active = fields.Boolean(
        string='Active',
        default=True,
        help="""Activate or Deactivate the print action button.
                If no active then move to the status \'archive\'.
                Still can by found using filters button""",
    )
    type = fields.Selection([
        ('gauge', 'Gauge'),
        ('counter', 'Counter'),        
        ('histogram', 'Histogram'),
        ('summary', 'Summary'),
    ], required=True, default='gauge')
    model_id = fields.Many2one(
        'ir.model',
        string='Model',
        required=True,
        ondelete='cascade',
    )
    model = fields.Char(
        string='Related Document Model',
        related='model_id.model',
        help="""Choose a model where the button is placed. You can find the
                model name in the URL. For example the model of this page is
                \'model=printnode.action.button\'.
                Check this in the URL after the \'model=\'.""",
    )
    domain = fields.Text(
        string='Domain',
        default='[]',
    )

    @api.constrains('name')
    def _validate_name(self):
        for rec in self:
            if ' ' in rec.name:
                raise ValidationError(_('Metric name must not contain spaces.'))
            if not str.islower(rec.name):
                raise ValidationError(_('Metric name must be lower case.'))
    
    def _get_model_count(self):
        self.ensure_one()
        related_model = self.env[self.model]
        domain = eval(self.domain)
        return related_model.search_count(domain)