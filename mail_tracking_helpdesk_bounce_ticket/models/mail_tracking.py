from odoo import models, fields, api

class MailTrackingEmail(models.Model):
    _inherit = 'mail.tracking.email'

    is_bounced_message = fields.Boolean(
        compute="_compute_is_bounced_message",
        store=True,
    )

    state = fields.Selection(
        [
            ("error", "Error"),
            ("deferred", "Deferred"),
            ("sent", "Sent"),
            ("delivered", "Delivered"),
            ("opened", "Opened"),
            ("rejected", "Rejected"),
            ("spam", "Spam"),
            ("unsub", "Unsubscribed"),
            ("bounced", "Bounced"),
            ("soft-bounced", "Soft bounced"),
        ],
        index=True,
        readonly=False,
        default=False,
        help=" * The 'Error' status indicates that there was an error "
        "when trying to sent the email, for example, "
        "'No valid recipient'\n"
        " * The 'Sent' status indicates that message was succesfully "
        "sent via outgoing email server (SMTP).\n"
        " * The 'Delivered' status indicates that message was "
        "succesfully delivered to recipient Mail Exchange (MX) server.\n"
        " * The 'Opened' status indicates that message was opened or "
        "clicked by recipient.\n"
        " * The 'Rejected' status indicates that recipient email "
        "address is blacklisted by outgoing email server (SMTP). "
        "It is recomended to delete this email address.\n"
        " * The 'Spam' status indicates that outgoing email "
        "server (SMTP) consider this message as spam.\n"
        " * The 'Unsubscribed' status indicates that recipient has "
        "requested to be unsubscribed from this message.\n"
        " * The 'Bounced' status indicates that message was bounced "
        "by recipient Mail Exchange (MX) server.\n"
        " * The 'Soft bounced' status indicates that message was soft "
        "bounced by recipient Mail Exchange (MX) server.\n",
    )

    @api.depends('state')
    def _compute_is_bounced_message(self):
        """Compute 'is_bounced_message' for each email based on its state."""
        for record in self:
            record.is_bounced_message = record.state in ['bounced', 'soft-bounced']

    def _create_helpdesk_ticket(self, email):
        message = self.env['mail.message'].search([('message_id', '=', email.message_id)], limit=1)
        if message:
            ticket_vals = {
                'name': 'Mail Delivery Issue',
                'description': f"Email with ID {email.message_id} has bounced.",
                'email': email.recipient,
                'message_ids': [(4, message.id)],  # Linking to existing messages
            }
            self.env['helpdesk.ticket'].create(ticket_vals)

    @api.model
    def create(self, vals):
        res = super(MailTrackingEmail, self).create(vals)
        for record in res.filtered('is_bounced_message'):
            self._create_helpdesk_ticket(record)
        return res

    def write(self, vals):
        res = super(MailTrackingEmail, self).write(vals)
        if 'state' in vals:
            for record in self.filtered('is_bounced_message'):
                self._create_helpdesk_ticket(record)
        return res
