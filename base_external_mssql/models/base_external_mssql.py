import logging
from contextlib import contextmanager
import pyodbc

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class BaseExternalMssql(models.Model):
    _name = 'base.external.mssql'
    _description = 'Base External Mssql'

    name = fields.Char("Name der Datenquelle", required=True)
    server = fields.Char("Datenbank-Server", required=True)
    database = fields.Char("Datenbank", required=True)
    username = fields.Char("Datenbank-User", required=True)
    password = fields.Char("Passwort", required=True)
    connection_string = fields.Text(readonly=True, compute="_compute_connection_string")
    priority = fields.Boolean(string='Verwenden')
    
    @api.depends("server", "database", "username", "password")
    def _compute_connection_string(self):
        for record in self:
            conn_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={record.server};DATABASE={record.database};UID={record.username};PWD={record.password};TrustServerCertificate=yes;'
            record.connection_string = conn_string

    
    @contextmanager
    def connection_open(self):
        """It provides a context manager for the data source."""
        try:
            connection = pyodbc.connect(self.connection_string)
            yield connection
        finally:
            try:
                self.connection_close(connection)
            except Exception:
                _logger.exception("Connection close failure.")

    def connection_close(self, connection):
        return connection.close()

    def execute(self, query_type, query, *params):
        # import pdb; pdb.set_trace()
        with self.connection_open() as connection:
            cur = connection.cursor()
            print("#### QUERY:", query)
            print("#### PARAMS:", params)
            
            cur.execute(query)
            if query_type == 'insert':
                connection.commit()
                res = cur.execute('SELECT SCOPE_IDENTITY() AS [SCOPE_IDENTITY];')
                print('res: ', res)
                last_id = res.fetchval()
                print('last_id:', last_id)
            elif query_type == 'select':
                rows = cur.fetchall()
                print('rows:', rows)
                return rows

            elif query_type == 'select_one':
                result = cur.fetchval()
                print('################ result:', result)
                connection.commit()
                return result


    def connection_test(self):
        """It tests the connection

        Raises:
            Validation message with the result of the connection (fail or success)
        """
        try:
            with self.connection_open():
                pass
        except Exception as e:
            raise ValidationError(
                "Connection test failed:\n" "Here is what we got instead:\n%s"
                % tools.ustr(e)
            )
        else:
            rows = self.execute('select', 'SELECT @@VERSION')
            message = "Datenbbank-Version:\n"
            for row in rows:
                message += f"{row[0]} \n"
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Datenbanktest erfolgreich',
                    'message': message,
                    'sticky': False,
                }
            }

    
    def set_priority(self):
        # Ensure only one record is selected
        if len(self) != 1:
            raise ValidationError("Bitte nur eine Datenbank verwenden.")
        
        # Set all records' priority to False
        self.search([]).write({'priority': False})
        
        # Set the selected record's priority to True
        self.write({'priority': True})
        
        return True
        