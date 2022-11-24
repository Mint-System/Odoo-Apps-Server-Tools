from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    can_impersonate_user = fields.Boolean(compute="_compute_can_impersonate_user")

    def _compute_can_impersonate_user(self):
        for user in self:
            user.can_impersonate_user = self.env.user.has_group('auth_impersonate_user.impersonate_user_group')

    def impersonate_user(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/web/impersonate?uid={}'.format(self.id),
        }
