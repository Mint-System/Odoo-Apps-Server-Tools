import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class IrActionsServer(models.Model):
    _inherit = "ir.actions.server"

    code = fields.Text(groups="base.group_erp_manager")
