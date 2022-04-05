from odoo.http import Controller, route
from prometheus_client import generate_latest


class PrometheusController(Controller):
    @route('/metrics', auth='public')
    def metrics(self):
        return generate_latest()