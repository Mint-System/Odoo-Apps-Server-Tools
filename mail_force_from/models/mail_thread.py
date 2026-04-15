# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _message_compute_author(self, author_id=None, email_from=None):
        author_id, email_from = super()._message_compute_author(author_id, email_from)

        # Lookup force from email for current model
        if self.env.user.company_id.alias_domain_id:
            force_from_email = self.env.user.company_id.alias_domain_id.get_force_from_email(model_name=self._name)
            if force_from_email:
                email_from = force_from_email

            _logger.warning([force_from_email])

        return author_id, email_from
