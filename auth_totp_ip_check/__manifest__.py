{
    "name": "Auth TOTP IP Check",
    "summary": """
        Disable totp for specific ip networks.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-workflow",
    "category": "Technical",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["auth_totp"],
    "data": ["views/auth_totp_cidr.xml", "security/ir.model.access.csv"],
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
