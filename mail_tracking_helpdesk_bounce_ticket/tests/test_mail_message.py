from odoo.tests import common

from odoo import _

class TestMailMessage(common.TransactionCase):
    def setUp(self):
        self.message = self.env["mail.message"].create({
            "subject": "Test Message",
            "body": "This is a test message",
        })

    def test_create_helpdesk_ticket(self):
        self.message.is_bounced_message = True
        self.message.message_type = "comment"
        self.message.subtype_id.name = "Discussions"
        self.message._create_helpdesk_ticket()
        ticket = self.env["helpdesk.ticket"].search([("name", "=", "Mail Delivery Issue")])
        self.assertTrue(ticket)
        message_body = _(
            "Email with ID %s has been bounced. This ticket has been created from: %s",
            self.message.id,
            self.message._get_html_link(),
        )
        message = self.env["mail.message"].search([("body", "=", message_body)])
        self.assertTrue(message)