import logging

from odoo import api, models, tools

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = "res.partner"

    @api.depends("name", "email")
    def _compute_email_formatted(self):
        """
        For mail name check parent name if partner name is not set.
        """
        super()._compute_email_formatted()
        for partner in self:
            emails_normalized = tools.email_normalize_all(partner.email)
            if emails_normalized:
                partner.email_formatted = tools.formataddr(
                    (
                        partner.name or partner.parent_id.name or "False",
                        ",".join(emails_normalized),
                    )
                )
            elif partner.email:
                partner.email_formatted = tools.formataddr(
                    (partner.name or partner.parent_id.name or "False", partner.email)
                )
