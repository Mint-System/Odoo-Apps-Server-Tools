import ipaddress
import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class TOTPCidr(models.Model):
    _name = "auth_totp.cidr"
    _description = "Allowed TOTP Cidr"

    user_ids = fields.Many2many("res.users", string="Users", ondelete="restrict")
    cidr = fields.Char()

    @api.constrains("cidr")
    def _validate_cidr(self):
        for rec in self:
            try:
                ipaddress.IPv4Network(rec.cidr)
            except:
                raise ValidationError(_("This is not a valid cidr."))
