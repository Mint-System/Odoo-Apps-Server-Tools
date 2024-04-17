from odoo import models, fields, api

class MailTrackingEmail(models.Model):
    _inherit = 'mail.tracking.email'


    @api.model
    def create(self, vals_list):
        records = super(MailTrackingEmail, self).create(vals_list)
        for record in records:
            if record.state in ['bounced', 'soft-bounced']:
                self.env['helpdesk.ticket'].create({
                    'name': 'Mail Delivery Failed',
                    'description': f"Email with ID {record.message_id} has failed to deliver.",
                    'email': record.recipient
                })
        return records


    def write(self, vals):
        res = super(MailTrackingEmail, self).write(vals)
        if vals.get('state') in ['bounced', 'soft-bounced']:
            for record in self:
                self.env['helpdesk.ticket'].create({
                    'name': 'Mail Delivery Failed',
                    'description': f"Email with ID {record.message_id} has failed to deliver.",
                    'email': record.recipient
                })
        return res
