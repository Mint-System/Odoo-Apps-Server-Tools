# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Auth Disable Password Login",
    "summary": """
        Disable password login for selected user.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "19.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["base"],
    "data": [
        "views/res_users_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
