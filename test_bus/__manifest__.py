# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Test Bus",
    "summary": """
        Simple test of Odoo Bus Service funcionality.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["base", "web", 'bus'],
    "data": [
        "security/ir.model.access.csv",
        "views/test_bus_model_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            'test_bus/static/src/components/*',
            'test_bus/static/src/js/bus_listener.js',
            'test_bus/static/src/js/bus_systray.js',
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    
}


