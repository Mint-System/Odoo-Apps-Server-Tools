import logging

from prometheus_client import CollectorRegistry, Counter, Gauge, generate_latest

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PrometheusController(http.Controller):
    @http.route(["/metrics"], auth="public", type="http", method=["GET"])
    def metrics(self):
        """
        Provide Prometheus metrics.
        """

        registry = CollectorRegistry()
        for metric in request.env["ir.metric"].sudo().search([]):
            if metric.type == "gauge":
                g = Gauge(metric.name, metric.description, registry=registry)
                g.set(metric._get_value())
            if metric.type == "counter":
                c = Counter(metric.name, metric.description, registry=registry)
                c.inc(metric._get_value())
        return generate_latest(registry)
