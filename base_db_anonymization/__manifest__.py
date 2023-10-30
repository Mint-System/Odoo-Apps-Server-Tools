{
    "name": "Base DB Anonymization",
    "summary": """
        Replace value of marked fields with fake data.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Administration",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["hr", "contacts"],
    "data": [
        "data/ir.model.access.csv",
        "data/ir_model_fields.xml",
        "views/ir_model_fields.xml",
        "views/ir_models_fields_anonymize.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
