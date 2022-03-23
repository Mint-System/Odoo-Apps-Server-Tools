from odoo import fields, models
 
class AuthOAuthProvider(models.Model): 
    _inherit = 'auth.oauth.provider' 
    x_keycloak = fields.Boolean(string='Keycloak')
