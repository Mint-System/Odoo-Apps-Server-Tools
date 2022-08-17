from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class Document(models.Model):
    _name = 'auth_totp_ip_check.document'
    _description = 'Auth totp ip check Document'

    # fields
    name = fields.Char()
    value = fields.Integer()