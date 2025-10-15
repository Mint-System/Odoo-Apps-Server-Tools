import logging

from odoo import models, tools

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
                email_to = tools.email_split_and_format(rec.email_to)
            rec["email_to"] = email_to
        return results
