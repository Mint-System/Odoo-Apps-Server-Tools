{
    "name": "Auth TOTP IP Check",
    "summary": """
        Disable totp for specific ip networks.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Technical",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["auth_totp"],
    "data": ["views/auth_totp_cidr.xml"],
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
