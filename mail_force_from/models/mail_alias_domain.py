# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class MailAliasDomain(models.Model):
    _inherit = "mail.alias.domain"

    force_from_ids = fields.One2many("mail.alias.domain.force_from", "domain_id")

    @api.model
    def get_force_from_email(self, model_name):
        force_from_id = self.force_from_ids.filtered(lambda f: f.model_name == model_name)[:1]
        if force_from_id:
            return f"{force_from_id.force_from}@{self.name}"
        else:
            return False
