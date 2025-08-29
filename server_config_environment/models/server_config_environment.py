import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import config

_logger = logging.getLogger(__name__)


class ServerConfigEnvironment(models.Model):
    _name = "server.config.environment"
    _description = "Server Config Environment"

    name = fields.Char(required=True)
    key = fields.Char(required=True)
    description = fields.Char(required=True)
    is_active = fields.Boolean(compute="_compute_is_active")
    default = fields.Boolean(help="Fallback to this environment if config['environment'] is not set.")

    def _compute_is_active(self):
        for rec in self:
            config_environment = config.get("environment")
            if config_environment and (rec.name == config_environment or rec.key == config_environment):
                rec.is_active = True
            else:
                rec.is_active = False

    @api.constrains("default")
    def _check_unique_default(self):
        if self.search_count([("default", "=", True)]) > 1:
            raise ValidationError(_("Only one environment can be set as default"))

    @api.model
    def get_active_environment(self):
        """
        Returns the active environment.
        """
        environment_id = self.search([]).filtered(lambda e: e.is_active)[:1]
        if not environment_id:
            environment_id = self.search([("default", "=", True)], limit=1)
        return environment_id
