{
    "name": "Prometheus Exporter",
    "summary": """
        Monitor Odoo metrics with Prometheus.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Technical",
    "version": "14.0.1.2.0",
    "license": "AGPL-3",
    "depends": ["mail", "resource"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_metric.xml",
        "views/ir_metric.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "external_dependencies": {
        "python": ["prometheus_client"],
    },
}
