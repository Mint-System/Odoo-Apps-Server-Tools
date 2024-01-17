import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    can_be_impersonated = fields.Boolean(compute="_compute_can_be_impersonated")
    can_impersonate_user = fields.Boolean(compute="_compute_can_impersonate_user")

    def _compute_can_impersonate_user(self):
        for user in self:
            user.can_impersonate_user = self.env.user.has_group(
                "auth_impersonate_user.impersonate_admin_group"
            )

    def _compute_can_be_impersonated(self):
        for user in self:
            user.can_be_impersonated = (
                user.has_group("auth_impersonate_user.impersonate_user_group")
                if self.env.user != user
                else False
            )

    def impersonate_user(self):
        self.ensure_one()
        if self.env.user.can_impersonate_user and self.can_be_impersonated:
            self._update_last_login()
            return {
                "type": "ir.actions.act_url",
                "target": "self",
                "url": "/web/impersonate?uid={}".format(self.id),
            }
