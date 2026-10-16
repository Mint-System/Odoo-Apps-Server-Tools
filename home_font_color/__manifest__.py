# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Home Font Color",
    "summary": """
        Define font color on home menu.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["base"],
    "data": [
        "views/res_company.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "assets": {
        "web.assets_backend": 
            [
                "home_font_color/static/src/webclient/**/*.scss",
                "home_font_color/static/src/webclient/**/*.js"
            ],
    },
    
}
