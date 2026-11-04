# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Web Font Georgia",
    "summary": """
        Add Georgia font to selection.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "20.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["web"],
    "data": [],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "assets": {
        "web.assets_backend": [
            "web_font_georgia/static/scss/fonts.scss",
        ],
        "web.report_assets_common": [
            "web_font_georgia/static/scss/fonts.scss",
        ],
    },
}
