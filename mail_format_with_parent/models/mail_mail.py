import logging

from odoo import models, tools

_logger = logging.getLogger(__name__)


class MailMail(models.Model):
    """Add the mass mailing campaign data to mail"""

    _inherit = ["mail.mail"]

    def _send_prepare_values(self, partner=None):
        """
        For mail name check parent name if partner name is not set.
        """
        self.ensure_one()
        res = super()._send_prepare_values(partner)
        if partner:
            emails_normalized = tools.email_normalize_all(partner.email)
            if emails_normalized:
                email_to = [
                    tools.formataddr(
                        (
                            partner.name or partner.parent_id.name or "False",
                            email or "False",
                        )
                    )
                    for email in emails_normalized
                ]
            else:
                email_to = [
                    tools.formataddr(
                        (
                            partner.name or partner.parent_id.name or "False",
                            partner.email or "False",
                        )
                    )
                ]
        else:
            email_to = tools.email_split_and_format(self.email_to)
        res["email_to"] = email_to
        return res
