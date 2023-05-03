from odoo import _, api, fields, models
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)
import ipaddress
import ast


class Users(models.Model):
    _inherit = 'res.users'

    totp_cidr_ids = fields.Many2many('auth_totp.cidr', ondelete='restrict')

    def _mfa_url(self):
        """Return if client ip is not in totp cidrs."""
        res = super()._mfa_url()

        # Get remote ip
        ip_address = ipaddress.IPv4Address(request.httprequest.environ['REMOTE_ADDR'])
        # Get cidrs from user
        allowed_cidrs = self.totp_cidr_ids
        # Get cidrs without users.
        allowed_cidrs += self.env['auth_totp.cidr'].search([('user_ids', '=', False)])
        # _logger.warning(['allowed_cidrs', allowed_cidrs])
        in_cidr = any(ip_address in cidr for cidr in allowed_cidrs.mapped(lambda r: ipaddress.IPv4Network(r.cidr)))

        # Check if user is allowed to login without totp
        prevent_login_without_2fa = ast.literal_eval(self.env["ir.config_parameter"].sudo().get_param("auth_totp.prevent_login_without_2fa", "False"))
        # _logger.warning([self.totp_enabled, prevent_login_without_2fa])
        if prevent_login_without_2fa and not self.totp_enabled and not in_cidr:
            return '/web/login'
        
        # Do not return url if ip is in allowed cidr list.
        if in_cidr:
            return
            
        return res


        