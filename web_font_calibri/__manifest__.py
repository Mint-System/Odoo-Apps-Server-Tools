# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Web Font Calibri",
    "summary": """
        Add Calibri to font selection.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "19.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["web"],
    "data": [],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "assets": {
        "web.assets_backend": [
            "web_font_calibri/static/scss/fonts.scss",
        ],
        "web.report_assets_common": [
            "web_font_calibri/static/scss/fonts.scss",
        ],
    },
}
