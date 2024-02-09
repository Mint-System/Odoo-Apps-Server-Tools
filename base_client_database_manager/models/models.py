import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class Base Client Database Manager(models.Model):
    _name = 'base_client_database_manager.document'
    _description = 'Base Client Database Manager Document'

    name = fields.Char()
    value = fields.Integer()