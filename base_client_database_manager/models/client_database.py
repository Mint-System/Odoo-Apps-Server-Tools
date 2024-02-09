from odoo import fields, models, api

class ClientDatabase(models.Model):
    _name = "client.database"
    _description = "Client's Database"
    # name = fields.Char("Title", required=True)
    # description = fields.Text("Description")

    name = fields.Char()
    url=fields.Char()
