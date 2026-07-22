import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class BusController(http.Controller):
    """Controller for handling bus-related requests."""

    @http.route("/test_bus/live_data", type="http", auth="user")
    def live_data(self, **kw):
        """
        Handle live data requests.
        """
        payload = kw or {"id": 999, "name": "Hello!"}
        # Send data to the listener.
        request.env["bus.bus"]._sendone("realtime-bus-test", "realtime-bus-test/sending-message", payload)
        _logger.info("Data sent to bus:", payload)
        return f"{payload['name']}"
