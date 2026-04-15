# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Mail Force From",
    "summary": """
        Setup and enforce multiple from addresses.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "19.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/mail_alias_domain_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
