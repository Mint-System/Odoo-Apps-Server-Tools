# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class MailMail(models.Model):
    _inherit = "mail.mail"

    def _split_by_mail_configuration(self):
        res = super()._split_by_mail_configuration()
        for mail_server_id, alias_domain_id, smtp_from, batch_ids in res:
            if alias_domain_id:
                alias_domain = self.env["mail.alias.domain"].sudo().browse(alias_domain_id)
                force_from_email = alias_domain.get_force_from_email(model_name=self[0].model)
                smtp_from = force_from_email
            yield mail_server_id, alias_domain_id, smtp_from, batch_ids
