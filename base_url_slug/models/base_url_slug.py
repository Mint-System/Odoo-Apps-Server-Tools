import re
import unicodedata

from odoo import api, fields, models


class BaseUrlSlugMixin(models.AbstractModel):
    _name = "base_url_slug.mixin"

    slug = fields.Char(compute="_compute_slug", store=True)

    @api.depends("name")
    def _compute_slug(self):
        for record in self:
            if record.name:
                record.slug = self._generate_slug(record.name)

    def _generate_slug(self, text):
        text = unicodedata.normalize("NFKD", text)
        text = re.sub(r"[^\w\s-]", "", text.lower())
        text = re.sub(r"[\s_-]+", "-", text).strip("-")
        return text
