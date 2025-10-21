import logging

from markupsafe import Markup

from odoo import models

_logger = logging.getLogger(__name__)


class DecimalAlign(models.AbstractModel):
    _name = "ir.qweb.field.decimal_align"
    _description = "QWeb field for decimal alignment of floats"
    _inherit = "ir.qweb.field"

    def value_to_html(self, value, options):
        if value is None:
            return ""

        decimals = int(options.get("decimals", 2)) if options else 2
        fmt = f"{{:.{decimals}f}}".format(value)
        if "." in fmt:
            int_part, frac_part = fmt.split(".")
        else:
            int_part, frac_part = fmt, ""

        html = (
            f'<span style="white-space:nowrap;text-align:right;display:inline-block;">'
            f'<span style="min-width:3em;display:inline-block;text-align:right;">{int_part}</span>'
            f'<span style="width:0.5em;display:inline-block;text-align:center;">.</span>'
            f'<span style="min-width:2em;display:inline-block;text-align:left;">{frac_part}</span>'
            f"</span>"
        )
        return Markup(html)
