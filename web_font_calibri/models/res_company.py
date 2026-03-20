# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class Company(models.Model):
    _inherit = "res.company"

    font = fields.Selection(selection_add=[("Calibri", "Calibri")])
