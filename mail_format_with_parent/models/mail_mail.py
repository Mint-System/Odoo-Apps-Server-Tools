import logging

from odoo import models, tools
from odoo.tools.mail import email_split_and_format

_logger = logging.getLogger(__name__)


class MailMail(models.Model):
    """Add the mass mailing campaign data to mail"""

    _inherit = ["mail.mail"]

    def _prepare_outgoing_list(self, mail_server=False, recipients_follower_status=None):
        """
        For mail name check parent name if partner name is not set.
        """
        results = super()._prepare_outgoing_list(mail_server, recipients_follower_status)
        for rec in results:
            partner_id = rec["partner_id"]
            if partner_id:
                emails_normalized = tools.email_normalize_all(partner_id.email)
                if emails_normalized:
                    email_to = [
                        tools.formataddr(
                            (
                                partner_id.name or partner_id.parent_id.name or "False",
                                email or "False",
                            )
                        )
                        for email in emails_normalized
                    ]
                else:
                    email_to = [
                        tools.formataddr(
                            (
                                partner_id.name or partner_id.parent_id.name or "False",
                                partner_id.email or "False",
                            )
                        )
                    ]
            else:
                raw_email_to = rec.get("email_to") or ""
                if isinstance(raw_email_to, list):
                    email_to = raw_email_to
                else:
                    email_to = email_split_and_format(raw_email_to)
            rec["email_to"] = email_to
        return results
