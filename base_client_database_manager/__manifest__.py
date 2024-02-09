{
    "name": "Base Client Database Manager",
    "summary": """
        Client view of databases.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Purchase,Technical,Accounting,Invoicing,Sales,Human Resources,Services,Helpdesk,Manufacturing,Website,Inventory,Administration,Productivity",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/client.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "images": ["images/screen.png"],
    }
