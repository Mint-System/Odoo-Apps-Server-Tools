{
    "name": "Home Background Image",
    "summary": """
        Set a background image for the Odoo company.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Customizations",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["base"],
    "data": ["views/base.xml"],
    "installable": True,
    "application": False,
    "images": ["images/screen.png"],
    "assets": {"web._assets_common_styles": ["home_background_image/static/src/scss/ui.scss"]},
}
