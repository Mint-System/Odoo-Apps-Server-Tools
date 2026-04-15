# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class MailAliasDomainForceFrom(models.Model):
    _name = "mail.alias.domain.force_from"
    _description = "Mail Alias Domain Force From"
    _rec_name = "force_from"

    force_from = fields.Char(
        required=True,
        help="Overwrites from address for selected model."
        "Must be a local-part e.g. 'support' and not a complete email address."
        "Ensure that mailbox can send as this address.",
    )
    domain_id = fields.Many2one("mail.alias.domain", required=True)
    model_id = fields.Many2one("ir.model")
    model_name = fields.Char(related="model_id.model")
