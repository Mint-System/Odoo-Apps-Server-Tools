{
    "name": "Auth Impersonate User",
    "summary": """
        Impersonate another users.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-workflow",
    "category": "Technical",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["web"],
    "demo": ["demo/res_users.xml"],
    "data": ["views/res_users.xml", "security/security.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
