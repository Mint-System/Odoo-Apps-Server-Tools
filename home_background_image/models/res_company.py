from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    background_image = fields.Binary(string="Home Background Image", attachment=True)
