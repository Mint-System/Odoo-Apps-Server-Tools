import logging

from odoo import api, fields, models

from odoo.addons.http_routing.models.ir_http import slugify

_logger = logging.getLogger(__name__)


class UrlSlugMixin(models.AbstractModel):
    _name = "url.slug.mixin"
    _description = "Url Slug Mix"

    slug = fields.Char("Url Slug", copy=False, compute="_compute_slug", store=True)

    @api.depends("name")
    def _compute_slug(self):
        for record in self:
            record.slug = slugify(record.name)
