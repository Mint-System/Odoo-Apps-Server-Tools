{
    "name": "Auth TOTP IP Check",
    "summary": """
        Disable totp for specific ip networks.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Technical",
    "version": "15.0.1.1.1",
    "license": "AGPL-3",
    "depends": ["auth_totp"],
    "data": ["views/auth_totp_cidr.xml", "security/ir.model.access.csv"],
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
