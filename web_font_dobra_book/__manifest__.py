# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Web Font Dobra Book",
    "summary": """
        Add free Web Font Dobra Book to font selection.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch",
    "category": "Repository",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["web"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "assets": {
        "web.assets_backend": [
            "web_font_dobra_book/static/scss/fonts.scss",
        ],
        "web.report_assets_common": [
            "web_font_dobra_book/static/scss/fonts.scss",
        ],
    },
}
