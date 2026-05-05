# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Test Bus",
    "summary": """
        Testing bus service
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "19.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["web", "base"],
    "data": [],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    'assets': {
    'web.assets_backend': [
        'test_bus/static/src/components/live_data.js',
        'test_bus/static/src/components/live_data.xml',
    ],
},
    
}
