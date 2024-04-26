import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class MailMessage(models.Model):
    _inherit = "mail.message"

    is_bounced_message = fields.Boolean(
        compute="_compute_is_bounced_message", store=True
    )

    @api.model
    def get_bounced_states(self):
        """The 'bounced' states of the message"""
        return {"bounced", "soft-bounced"}

    @api.depends(
        "mail_tracking_ids.state",
    )
    def _compute_is_bounced_message(self):
        """Compute 'is_bounced_message' field for the active user"""
        bounced_states = self.get_bounced_states()
        for message in self:
            has_bounced_trackings = bounced_states.intersection(
                message.mapped("mail_tracking_ids.state")
            )
            message.is_bounced_message = has_bounced_trackings

            if (
                message.is_bounced_message
                and message.message_type == "comment"
                and message.subtype_id.name == "Discussions"
            ):
                self._create_helpdesk_ticket()

    def _create_helpdesk_ticket(self):
        ticket_vals = {
            "name": _("Mail Delivery Issue"),
            "description": _("Email with ID %s has been bounced.", self.id),
        }
        ticket_id = self.env["helpdesk.ticket"].create(ticket_vals)

        body = _(
            "This ticket has been created from %s",
            self._get_html_link(),
        )
        ticket_id.with_context(**{"mail_notrack": True}).message_post(body=body)
