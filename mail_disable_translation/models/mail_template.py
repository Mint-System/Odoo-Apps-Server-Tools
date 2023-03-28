from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    name = fields.Char(translate=False)