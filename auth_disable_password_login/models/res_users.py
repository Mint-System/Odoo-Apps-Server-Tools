# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models
from odoo.exceptions import AccessDenied

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"


    disable_password_login = fields.Boolean(
        default=False,
        store=True,
    )


    def _crypt_context(self):
        if self.disable_password_login:
            raise AccessDenied(_("Password login is disabled"))

        return super()._crypt_context()