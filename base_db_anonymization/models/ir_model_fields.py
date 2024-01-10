import ast
import logging
import random

from odoo import _, api, fields, models
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)


class IrModelField(models.Model):
    _inherit = "ir.model.fields"

    anonymize_id = fields.Many2one(
        "ir.model.fields.anonymize", compute="_compute_anonymize_id"
    )

    def _compute_anonymize_id(self):
        anonymize_ids = self.env["ir.model.fields.anonymize"].search([])
        for field in self:
            anonymize_id = anonymize_ids.filtered(lambda a: a.field_id.id == field.id)[
                :1
            ]
            field.anonymize_id = anonymize_id.id if anonymize_ids else False


class IrModelFieldAnonymize(models.Model):
    _name = "ir.model.fields.anonymize"
    _description = "Anonymization Configuration"

    active = fields.Boolean(default=True)
    name = fields.Char(related="field_id.name")
    model = fields.Char(related="field_id.model")
    model_id = fields.Many2one(
        "ir.model", compute="_compute_model_id", store=True, readonly=False
    )
    field_id = fields.Many2one("ir.model.fields", copy=False)
    field_type = fields.Selection(related="field_id.ttype")
    anonymize_strategy = fields.Selection(
        [
            ("xml_id", "XML ID"),
            ("value", "Value"),
            ("random", "Random"),
            ("clear", "Clear"),
        ],
        help="Anonymiztion strategy. \n"
        "- xml_id: Concat model name and database id.\n"
        "- value: Enter a value that is applied to all records.\n"
        "- random: Generate random values based on data type.\n"
        "- clear: Clear field content.",
    )
    domain = fields.Char(required=True, default="[]")
    anonymize_value = fields.Char(default="Lorem Ipsum {rec.id}")
    anonymize_random_range = fields.Char(help="Format: start, stop")
    output_new_value = fields.Boolean(string="Output to Server Log")
    is_anonymized = fields.Boolean()

    @api.depends("field_id")
    def _compute_model_id(self):
        for anon in self:
            anon.model_id = anon.field_id.model_id

    def action_anonymize_records(self):
        messages = []
        if not self.env.user.has_group("base_db_anonymization.can_anonymize_records"):
            raise AccessError(_("User is not allowed to anonymize records."))

        for anon in self.filtered(lambda a: not a.is_anonymized):
            domain = ast.literal_eval(anon.domain)
            records = self.env[anon.field_id.model].search(domain)
            fieldname = anon.field_id.name
            fieldtype = anon.field_id.ttype

            _logger.warning(
                _("Anonymize feld '%s' of model '%s'.") % (anon.name, anon.model)
            )

            # ID strategy
            if anon.anonymize_strategy == "xml_id":
                for rec in records:
                    new_value = (
                        anon.field_id.model.replace(".", "_") + "_" + str(rec.id)
                    )
                    if anon.output_new_value:
                        messages.append(
                            fieldname
                            + ": "
                            + getattr(rec, fieldname, "-")
                            + "  >>>  "
                            + str(new_value)
                        )
                    rec.write({fieldname: new_value})

            # Random strategy
            if anon.anonymize_strategy == "random":
                for rec in records:
                    new_value = random.randrange(
                        *map(int, anon.anonymize_random_range.split(", "))
                    )
                    if anon.output_new_value:
                        messages.append(
                            fieldname
                            + ": "
                            + getattr(rec, fieldname, "-")
                            + "  >>>  "
                            + str(new_value)
                        )
                    rec.write({fieldname: new_value})

            # Value strategy
            if anon.anonymize_strategy == "value":
                for rec in records:
                    new_value = anon.anonymize_value
                    new_value = int(new_value) if fieldtype == "integer" else new_value
                    new_value = float(new_value) if fieldtype == "float" else new_value
                    new_value = bool(new_value) if fieldtype == "boolean" else new_value
                    if anon.output_new_value:
                        messages.append(
                            fieldname
                            + ": "
                            + str(getattr(rec, fieldname, "-"))
                            + "  >>>  "
                            + str(new_value)
                        )
                    rec.write({fieldname: new_value})

            # Clear strategy
            if anon.anonymize_strategy == "clear":
                records.write({fieldname: False})

            anon.write({"is_anonymized": True})

        if messages:
            _logger.warning(_("New values:\n") + "\n".join(messages))
