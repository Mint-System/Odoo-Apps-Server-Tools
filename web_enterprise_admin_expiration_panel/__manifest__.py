{
    "name": "Web Enterprise Admin Expiration Panel",
    "summary": """
        Show database expiration panel for Admins only.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Administration",
    "version": "16.0.1.0.0",
    "license": "OPL-1",
    "depends": ["web_enterprise"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "assets": {
        "web.assets_backend": [
            "web_enterprise_admin_expiration_panel/static/src/js/*.js",
            "web_enterprise_admin_expiration_panel/static/src/js/*.xml",
        ],
    },
}
