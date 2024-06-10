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
        subtype_id = self.env.ref("mail.mt_comment")

        for message in self:
            has_bounced_trackings = bounced_states.intersection(
                message.mapped("mail_tracking_ids.state")
            )
            message.is_bounced_message = has_bounced_trackings
            
            if (
                message.is_bounced_message
                and message.message_type == "comment"
                and message.subtype_id == subtype_id
            ):
                message._create_helpdesk_ticket()

    def _create_helpdesk_ticket(self):
        self.ensure_one()
        ticket_id = self.env["helpdesk.ticket"].create({
            "name": _("Mail Delivery Issue"),
            "partner_id": self.partner_ids[0].id if self.partner_ids else False,
        })
        message_body = _(
            "Email with ID %s has been bounced. This ticket has been created from: %s",
            self.id,
            self._get_html_link(),
        )
        ticket_id.message_post(body=message_body, message_type="notification")
