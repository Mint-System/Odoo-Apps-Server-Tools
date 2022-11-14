import json

import requests

from odoo import api, fields, models
from odoo.exceptions import AccessDenied, UserError
from odoo.addons.auth_signup.models.res_users import SignupError

from odoo.addons import base
base.models.res_users.USER_PRIVATE_FIELDS.append('oauth_access_token')

class ResUsers(models.Model):
    _inherit = 'res.users'

    oauth_provider_id = fields.Many2one('auth.oauth.provider', string='OAuth Provider')
    oauth_uid = fields.Char(string='OAuth User ID', help="Oauth Provider user_id", copy=False)
    oauth_access_token = fields.Char(string='OAuth Access Token', readonly=True, copy=False)

    _sql_constraints = [
        ('uniq_users_oauth_provider_oauth_uid', 'unique(oauth_provider_id, oauth_uid)', 'OAuth UID must be unique per provider'),
    ]

    @api.model
    def _auth_oauth_rpc(self, endpoint, access_token):
        return requests.get(endpoint, params={'access_token': access_token}).json()
    
    def _auth_oauth_rpc(self, endpoint, access_token, provider):
        oauth_provider = self.env['auth.oauth.provider'].browse(provider)
        if oauth_provider.x_keycloak:
          return requests.get(endpoint, headers={'Authorization': 'bearer ' + access_token}).json()
        else:
          return requests.get(endpoint, params={'access_token': access_token}).json()
    
    @api.model
    def _auth_oauth_validate(self, provider, access_token):
        """ return the validation data corresponding to the access token """
        oauth_provider = self.env['auth.oauth.provider'].browse(provider)
        validation = self._auth_oauth_rpc(oauth_provider.validation_endpoint, access_token, provider)
        if validation.get("error"):
            raise Exception(validation['error'])
        if oauth_provider.data_endpoint:
            data = self._auth_oauth_rpc(oauth_provider.data_endpoint, access_token, provider)
            validation.update(data)
        return validation