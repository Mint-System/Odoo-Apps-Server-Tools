{
    "name": "Monitoring Prometheus Exporter",
    "summary": """
        Export Odoo digest kpis as Prometheus metrics.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Tools",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["web"],
    "external_dependencies": {
        "python": ["prometheus_client"]
    },
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}