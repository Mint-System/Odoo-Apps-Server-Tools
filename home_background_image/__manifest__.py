{
    "name": "Home Background Image",
    "summary": """
        Set a background image for the Odoo company.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Customizations",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["base"],
    "data": ["views/base.xml"],
    "installable": True,
    "application": False,
    "images": ["images/screen.png"],
    "assets": {
        "web.assets_backend": ["home_background_image/static/src/webclient/**/*.scss"],
    },
}
