
from odoo import models
from odoo.http import request
from prometheus_client import Summary, Counter


REQUEST_TIME = Summary(
    "request_latency_sec", "Request response time in sec", ["query_type"]
)
LONGPOLLING_COUNT = Counter("longpolling", "Longpolling request count")


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _dispatch(cls):
        path_info = request.httprequest.environ.get("PATH_INFO")

        if path_info.startswith("/longpolling/"):
            LONGPOLLING_COUNT.inc()
            return super()._dispatch()

        if path_info.startswith("/metrics"):
            return super()._dispatch()

        if path_info.startswith("/web/static"):
            label = "assets"
        elif path_info.startswith("/web/content"):
            label = "filestore"
        else:
            label = "client"

        res = None
        with REQUEST_TIME.labels(label).time():
            res = super()._dispatch()

        return res