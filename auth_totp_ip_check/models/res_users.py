from odoo import _, api, fields, models
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)
import ipaddress



class Users(models.Model):
    _inherit = 'res.users'

    totp_cidr_ids = fields.Many2many('auth_totp.cidr', ondelete='restrict')

    def _mfa_url(self):
        res = super()._mfa_url()
        # Get remote ip
        ip_address = ipaddress.IPv4Address(request.httprequest.environ['REMOTE_ADDR'])
        # Do not return url if ip is in allowed cidr list.
        if any(ip_address in cidr for cidr in self.totp_cidr_ids.mapped(lambda r: ipaddress.IPv4Network(r.cidr))):
            return
        return res