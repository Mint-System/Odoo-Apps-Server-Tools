from odoo import _, fields, models
import logging
_logger = logging.getLogger(__name__)


class IrMailServer(models.Model):
    _inherit = ['ir.mail_server']

    database_filter = fields.Char()

    def _find_mail_server(self, email_from, mail_servers=None):
        """Apply database filter"""
        if mail_servers is None:
            mail_servers = self.sudo().search([], order='sequence')
        db_name = self._cr.dbname
        mail_servers = mail_servers.filtered(lambda s: not s.database_filter or (db_name in s.database_filter.split(',')))
        return super()._find_mail_server(email_from, mail_servers)
