from odoo import fields, models, api

class ClientServer(models.Model):
    _name = "client.server"
    _description = "Server for client's Odoo instance"
    # name = fields.Char("Title", required=True)
    # description = fields.Text("Description")

    name = fields.Char()
    hostname = fields.Char()
    hosting_partner_id = fields.Many2one(
        "res.partner", "Hosting Provider"
    )

    database_ids = fields.Many2one(
        "client.database", "Client's Database ID"
    )
