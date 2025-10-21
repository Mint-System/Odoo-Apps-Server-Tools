# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Web Font Manrope",
    "summary": """
        Add Manrope font to selection.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Administration",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["web"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "assets": {
        "web.assets_backend": [
            "web_font_manrope/static/scss/fonts.scss",
        ],
        "web.report_assets_common": [
            "web_font_manrope/static/scss/fonts.scss",
        ],
    },
}
