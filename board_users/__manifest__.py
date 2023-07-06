{
    "name": "Board Users",
    "summary": """
        See all dashboards of each user.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Tools",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["board"],
    "data": [
        "views/board_users_view.xml",
        "security/board_users.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": False,
    "images": ["images/screen.png"],
    "assets": {
        "web.assets_backend": [
            "board_users/static/src/js/abstract_controller_inherit.js",
        ],
    },
}
