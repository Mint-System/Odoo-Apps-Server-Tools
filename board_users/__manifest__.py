{
    "name": "Board Users",
    "summary": """
        See all dashboards of each user.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Tools",
    "version": "14.0.1.1.0",
    "license": "AGPL-3",
    "depends": ["board"],
    "data": [
        "views/board_users_view.xml",
        "security/board_users.xml",
        "security/ir.model.access.csv",
        "views/assets_backend.xml",
    ],
    "installable": True,
    "application": False,
    "images": ["images/screen.png"],
}
