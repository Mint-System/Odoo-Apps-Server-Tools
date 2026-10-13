import logging
from contextlib import contextmanager

import pymssql
import pyodbc

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

# this is need otherwise pyodbc will not work correctly
pyodbc.setDecimalSeparator(".")


class BaseExternalMssql(models.Model):
    _name = "base.external.mssql"
    _description = "Base External Mssql"

    name = fields.Char("Name of Datasource", required=True)
    server = fields.Char("Datenbase Server", required=True)
    database = fields.Char("Database Name", required=True)
    username = fields.Char("Database User", required=True)
    password = fields.Char("Database Password", required=True)
    connection_string = fields.Text(readonly=True, compute="_compute_connection_string")
    priority = fields.Boolean(string="Use this DB")
    driver = fields.Selection([("pyodbc", "pyodbc"), ("pymssql", "pymssql")], default="pymssql")
    database_type = fields.Selection([("interface", "Interface"), ("proddb", "Prod DB")], default="interface")
    use_button_is_visible = fields.Boolean(
        string="Use DB Button Visibility", compute="_compute_use_button_is_visible", store=False
    )

    @api.depends("priority")
    def _compute_use_button_is_visible(self):
        for record in self:
            record.use_button_is_visible = not record.priority

    @api.constrains("priority", "database_type")
    def _check_one_priority_per_database_type(self):
        for record in self.filtered("priority"):
            if self.search_count([("database_type", "=", record.database_type), ("priority", "=", True)]) > 1:
                raise ValidationError(_("Only one data source of type %s can be used.", record.database_type))

    @api.model
    def _get_by_database_type(self, database_type):
        """The data source to use for a database type: the one with priority, or the only one.

        Returns an empty recordset if there are several and none has priority.
        """
        sources = self.search([("database_type", "=", database_type)], order="priority desc, id")
        if len(sources) > 1 and not sources[0].priority:
            _logger.warning("Several data sources of type %s, but none is used.", database_type)
            return self.browse()
        return sources[:1]

    @api.depends("server", "database", "username", "password")
    def _compute_connection_string(self):
        for record in self:
            if record.driver == "pyodbc":
                conn_string = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={record.server};\
                                DATABASE={record.database};UID={record.username};\
                                PWD={record.password};TrustServerCertificate=yes;"
            elif record.driver == "pymssql":
                conn_string = f'server="{record.server}", user="{record.username}",\
                                password="{record.password}", \
                                database="{record.database}", tds_version="7.0"'

            record.connection_string = conn_string

    @contextmanager
    def connection_open(self):
        """It provides a context manager for the data source."""
        try:
            if self.driver == "pyodbc":
                connection = pyodbc.connect(self.connection_string, autocommit=True)
            elif self.driver == "pymssql":
                connection = pymssql.connect(
                    server=self.server,
                    user=self.username,
                    password=self.password,
                    database=self.database,
                    tds_version="7.0",
                    autocommit=True,
                )
            yield connection
        finally:
            try:
                self.connection_close(connection)
            except Exception:
                _logger.exception("Connection close failure.")

    def connection_close(self, connection):
        return connection.close()

    def _get_db_driver(self):
        return self.driver

    def execute(self, query_type, query, *params, as_dict=True):
        with self.connection_open() as connection:
            cursor_factory = connection.cursor if not as_dict else lambda: connection.cursor(as_dict=True)
            cur = cursor_factory()

            # _logger.info("Executing query: %s | Params: %s", query, params)
            # if not as_dict:
            #     cur = connection.cursor()
            # else:
            #     cur = connection.cursor(as_dict=True)
            # _logger.info("Executing query: %s" % (query,))
            # cur.execute(query)
            if params:
                cur.execute(query, *params)
                # _logger.info("Executing query: %s | Params: %s", query, params)
            else:
                cur.execute(query)
                # _logger.info("Executing query: %s", query)

            if query_type == "insert":
                # connection.commit() not needed for pymssql
                # this works for pyodbc:
                # res = cur.execute('SELECT SCOPE_IDENTITY() AS [SCOPE_IDENTITY];')
                # last_id = res.fetchval() # this works for pyodbc
                connection.commit()

                try:
                    return cur.lastrowid
                except AttributeError:
                    # Fallback for drivers that don’t support lastrowid
                    cur.execute("SELECT SCOPE_IDENTITY();")
                    return cur.fetchone()[0]
                # last_id = cur.lastrowid
                # return last_id
            elif query_type == "select":
                rows = cur.fetchall()
                return rows

            elif query_type == "select_one":
                # result = cur.fetchval()
                # result = cur.fetchone()[0]
                result = cur.fetchone()
                # _logger.info("RESULT FROM SELECT ONE: %s" % (result,))
                connection.commit()
                return result

            elif query_type in ("update", "delete"):
                connection.commit()
                return cur.rowcount  # Optional: return number of affected rows

            else:
                raise ValueError(f"Unsupported query_type: {query_type}")

    def connection_test(self):
        """It tests the connection

        Raises:
            Validation message with the result of the connection (fail or success)
        """
        try:
            with self.connection_open():
                pass
        except Exception as e:
            raise ValidationError(_("Connection test failed:\nHere is what we got instead:\n%s") % tools.ustr(e)) from e
        else:
            rows = self.execute("select", "SELECT @@VERSION", as_dict=False)
            message = _("Database Version:\n")
            for row in rows:
                message += f"{row[0]} \n"

            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Connection Test successful"),
                    "message": message,
                    "sticky": False,
                },
            }

    def set_priority(self):
        """Use this data source instead of the others of the same database type."""
        if len(self) != 1:
            raise ValidationError(_("Please use only one database."))

        (self.search([("database_type", "=", self.database_type)]) - self).write({"priority": False})
        self.write({"priority": True})

        return True
