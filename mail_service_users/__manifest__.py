{
    "name": "Mail Service Users",
    "summary": """
        Exclude service users from warranty contract.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Technical",
    "version": "18.0.1.0.0",
    "license": "OPL-1",
    "depends": ["web_enterprise", "mail"],
    "data": ["views/base.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "assets": {
        "web.assets_backend": [
            "mail_service_users/static/src/enterprise_subscription_service.js",
        ],
    },
}
