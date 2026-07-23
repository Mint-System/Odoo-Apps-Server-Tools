# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Mail Server Filter Model",
    "summary": """
        Restrict mail server to messages connected to allowed data model.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "19.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["mail"],
    "data": [
        "views/ir_mail_server.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
