from odoo import fields, models


class User(models.Model):
    _inherit = "res.users"

    service_user = fields.Boolean(default=False)
