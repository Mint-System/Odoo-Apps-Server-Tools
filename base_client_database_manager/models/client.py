from odoo import models, fields

class ClientServer(models.Model):
    _name = 'client.server'
    _description = 'Client Server'

    name = fields.Char("Server Name", required=True)
    hostname = fields.Char("Hostname")
    hosting_partner_id = fields.Many2one('res.partner', string="Hosting Partner")
    database_ids = fields.One2many('client.database', 'server_id', string="Databases")

class ClientDatabase(models.Model):
    _name = 'client.database'
    _description = 'Client Database'

    name = fields.Char("Database Name", required=True)
    url = fields.Char("Database URL")
    db_type = fields.Selection([
        ('production', 'Production'),
        ('development', 'Development'),
        ('staging', 'Staging')
    ], string="Type", default='development')
    is_active = fields.Boolean("Is Active?", default=True)
    server_id = fields.Many2one('client.server', string="Server", required=True)
    container_id = fields.Char("Container ID")



# from odoo import models, fields

# class ClientServer(models.Model):
#     _name = 'client.server'
#     _description = 'Client Server'

#     name = fields.Char("Database Name", required=True)
#     hostname = fields.Char("Hostname")
#     hosting_partner_id = fields.Many2one('res.partner', string="Hosting Partner")
#     database_ids = fields.One2many('client.database', 'server_id', string="Databases")

# class ClientDatabase(models.Model):
#     _name = 'client.database'
#     _description = 'Client Database'

#     name = fields.Char("Name", required=True)
#     url = fields.Char("Database URL")
#     server_id = fields.Many2one('client.server', string="Server", required=True)
