# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = "res.company"


    home_font_color = fields.Char(
        string="Home Font Color",
        default="#FFFFFF",
    )


    @api.model
    def get_home_font_color(self):
        color = self.env.company.home_font_color
        return color
