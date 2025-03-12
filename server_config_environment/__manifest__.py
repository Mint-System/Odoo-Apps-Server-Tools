{
    "name": "Config Environment",
    "summary": """
        Define environments for server configurations.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Technical",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["base"],
    "data": [
        "data/data.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/server_config_environment_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
