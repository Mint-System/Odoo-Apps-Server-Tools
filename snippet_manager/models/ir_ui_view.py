import logging

import requests

from odoo import _, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    def update_from_source(self):
        """
        Update view from source.
        Fetches the view definition from: {source_url}/{self.name}.xml and copies to arch field.
        Only updates existing views, does not create new views.
        """
        # Get the source URL from system parameter
        source_url = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("snippet_manager.source_url", "https://odoo.build/snippets/")
        )

        if not self.name:
            raise UserError(_("View name is required"))

        # Get view definition from URL
        url = f"{source_url.rstrip('/')}/{self.name}.xml"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                view_xml = response.text
                _logger.info(f"Fetched view definition for '{self.name}' from {url}")

                # Update the arch field of current view (self)
                self.write({"arch": view_xml})
                _logger.info(f"Updated view '{self.name}' arch from {url}")
                return {"result": "updated", "view_id": self.id, "view_name": self.name, "source": "URL"}
            else:
                raise UserError(
                    _(f"View definition for '{self.name}' not found at {url} (HTTP {response.status_code})")
                )
        except requests.RequestException as e:
            _logger.error(f"Could not fetch view from URL {url}: {e}")
            raise UserError(_(f"Could not fetch view definition from {url}: {e}"))
        except Exception as e:
            _logger.error(f"Unexpected error when fetching view from URL {url}: {e}")
            raise UserError(_(f"Unexpected error when fetching view from {url}: {e}"))
