import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class FetchmailServer(models.Model):
    _inherit = ["fetchmail.server"]

    database_filter = fields.Char()

    def fetch_mail(self):
        """Apply database filter"""
        db_name = self._cr.dbname
        server = self.filtered(
            lambda s: not s.database_filter or (db_name in s.database_filter.split(","))
        )
        return super(FetchmailServer, server).fetch_mail()
