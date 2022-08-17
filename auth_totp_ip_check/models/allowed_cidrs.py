from odoo import models, fields
import ipaddress
from odoo.exceptions import ValidationError


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    totp_cidr_ids = fields.One2many('auth_totp.cidr', ondelete='restrict')

class Totpidr(models.Model):
    _name = 'auth_totp.cidr'

    user_ids = fields.Many2many('res.users', ondelete='restrict')
    cidr = fields.Char(string='cidr')

    @api.constrains('cidr')
    def _validate_cidr(self):
        for rec in self:
            try:
                ipaddress.IPv4Network(rec.cidr)
            except:
                raise ValidationError(_("%s is not a valid cidr.") % (rec.cidr, rec.age_from, rec.age_to))