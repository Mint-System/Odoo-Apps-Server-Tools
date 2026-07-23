from odoo import http
from odoo.http import request


class TestController(http.Controller):
    @http.route("/test_bus/simple", auth="public")
    def simple_test(self, **kw):
        return "<div>ok</div>"

    @http.route("/test_bus/live_data", type="jsonrpc", auth="public")
    # def live_data(self, **kw):
    #     live_data = {'id': 1, 'name': 'Live Data from Backend'}
    #     channel = "your_channel"
    #     # Send to bus service
    #     request.env["bus.bus"]._sendone(channel, "notification", message=live_data)
    #     return {'result': 'Live data sent successfully'}
    def live_data(self, **kw):
        live_data = {"id": 1, "name": "Live Data from Backend"}
        channel = (request.env.cr.dbname, "my_channel")  # tuple format
        request.env["bus.bus"]._sendone(channel, "notification", live_data)
        return {"result": "Live data sent successfully"}
