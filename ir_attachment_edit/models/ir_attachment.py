from odoo import fields, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    res_model = fields.Char(readonly=False)
    res_field = fields.Char(readonly=False)
    res_id = fields.Many2oneReference(readonly=False)
