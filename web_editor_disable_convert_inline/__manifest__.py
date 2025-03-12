{
    "name": "Web Editor Disable Convert Inline",
    "summary": """
        Disable inline conversion in Odoo editor.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Technical",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["web"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "assets": {
        "web.assets_backend": [
            "web_editor_disable_convert_inline/static/src/js/backend/**/*",
        ],
    },
}
