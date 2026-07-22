# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    model_ids = fields.Many2many(
        'ir.model', 
        string="Allowed Models", 
        help="This server will only be used to send emails"
             "related to these models",
        )

