{
    "name": "Base DB Anonymization",
    "summary": """
        Anonymize content of selected database fields.
    """,
    "author": "Mint System GmbH",
    "website": "https://github.com/Mint-System/template",
    "category": "Administration",
    "version": "16.0.1.4.0",
    "license": "AGPL-3",
    "depends": ["hr", "contacts"],
    "demo": ["demo/res_groups.xml"],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "data/ir_model_fields.xml",
        "views/ir_model_fields.xml",
        "views/ir_models_fields_anonymize.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
