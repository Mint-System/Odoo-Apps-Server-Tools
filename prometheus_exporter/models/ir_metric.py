import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)
from odoo.exceptions import ValidationError


class Metric(models.Model):
    _name = "ir.metric"
    _description = "Metrics"

    name = fields.Char(required=True)
    description = fields.Char()
    active = fields.Boolean(
        string="Active",
        default=True,
        help="""Activate or Deactivate the print action button.
                If no active then move to the status \'archive\'.
                Still can by found using filters button""",
    )
    type = fields.Selection(
        [
            ("gauge", "Gauge"),
            ("counter", "Counter"),
            ("histogram", "Histogram"),
            ("summary", "Summary"),
        ],
        required=True,
        default="gauge",
    )
    model_id = fields.Many2one(
        "ir.model",
        string="Model",
        required=True,
        ondelete="cascade",
    )
    model = fields.Char(
        string="Related Document Model",
        related="model_id.model",
        help="""Choose a model where the button is placed. You can find the
                model name in the URL. For example the model of this page is
                \'model=printnode.action.button\'.
                Check this in the URL after the \'model=\'.""",
    )
    domain = fields.Text(
        string="Domain",
        default="[]",
    )
    field_id = fields.Many2one(
        "ir.model.fields",
        "Measured Field",
        domain="[('store', '=', True), ('model_id', '=', model_id), ('ttype', 'in', ['float','integer','monetary'])]",
    )
    field = fields.Char(related="field_id.name")
    operation = fields.Selection(
        [
            ("sum", "Sum"),
            ("avg", "Average"),
            ("count", "Count"),
            ("min", "Min"),
            ("max", "Max"),
        ],
        default="sum",
    )

    @api.constrains("name")
    def _validate_name(self):
        for rec in self:
            if " " in rec.name:
                raise ValidationError(_("Metric name must not contain spaces."))
            if not str.islower(rec.name):
                raise ValidationError(_("Metric name must be lower case."))

    def _get_model_count(self):
        """Count model records."""
        self.ensure_one()
        related_model = self.env[self.model]
        domain = eval(self.domain)
        return related_model.search_count(domain)

    def _get_field_value(self):
        """Run operation for selected field."""
        self.ensure_one()
        related_model = self.env[self.model]
        domain = eval(self.domain)
        operation = self.operation
        if self.field_id:
            records = related_model.search(domain)
            values = records.mapped(self.field)
            if operation == "avg":
                return avg(values)
            elif operation == "sum":
                return sum(values)
            elif operation == "count":
                return len(values)
            elif operation == "min":
                return min(values)
            elif operation == "max":
                return max(values)
        else:
            return 0

    def _get_value(self):
        """Generic method to return metric value."""
        if self.field_id:
            return self._get_field_value()
        else:
            return self._get_model_count()
