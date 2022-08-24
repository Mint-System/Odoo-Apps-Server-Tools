from odoo import models, fields, api
import ipaddress
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class TOTPCidr(models.Model):
    _name = 'auth_totp.cidr'
    _description = 'Allowed TOTP Cidr'

    user_ids = fields.Many2many('res.users',string='Users', ondelete='restrict')
    cidr = fields.Char(string='Cidr')

    @api.constrains('cidr')
    def _validate_cidr(self):
        for rec in self:
            try:
                ipaddress.IPv4Network(rec.cidr)
            except:
                raise ValidationError(_("%s is not a valid cidr.") % (rec.cidr, rec.age_from, rec.age_to))