import logging


from odoo import models

_logger = logging.getLogger(__name__)

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super().session_info()
        _logger.info("### session_info override called")
        if self.env.user._is_internal():
            result['home_font_color'] = self.env.company.home_font_color
        return result