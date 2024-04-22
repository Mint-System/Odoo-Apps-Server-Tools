{
    "name": "Base Client Database Manager",
    "summary": """
        Client view of databases.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Administration",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["base", "web", "portal"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/client.xml",
        "views/portal.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "images": ["images/screen.png"],
    }
