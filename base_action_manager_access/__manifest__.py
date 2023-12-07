{
    "name": "Base Action Manager Access",
    "summary": """
        Grant server action access to erp manager group.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Administration",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["base_automation"],
    "data": [
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
