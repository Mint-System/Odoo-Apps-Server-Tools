from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestPriority(TransactionCase):
    """Of several data sources of the same database type, the one with priority is used."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Source = cls.env["base.external.mssql"]
        cls.Source.search([]).unlink()
        cls.sdb_live = cls._create("SDB live", "interface")
        cls.sdb_test = cls._create("SDB test", "interface")
        cls.proddb_live = cls._create("ProdDB live", "proddb")
        cls.proddb_test = cls._create("ProdDB test", "proddb")

    @classmethod
    def _create(cls, name, database_type):
        return cls.Source.create(
            {
                "name": name,
                "server": "localhost",
                "database": name,
                "database_type": database_type,
                "username": "odoo",
                "password": "secret",
            }
        )

    def test_priority_is_set_per_database_type(self):
        self.sdb_test.set_priority()
        self.proddb_live.set_priority()

        self.assertEqual(self.Source._get_by_database_type("interface"), self.sdb_test)
        self.assertEqual(self.Source._get_by_database_type("proddb"), self.proddb_live)

        self.sdb_live.set_priority()
        self.assertFalse(self.sdb_test.priority)
        self.assertTrue(self.proddb_live.priority)

    def test_only_source_of_a_database_type_is_used_without_priority(self):
        self.sdb_test.unlink()
        self.assertEqual(self.Source._get_by_database_type("interface"), self.sdb_live)

    def test_no_source_is_used_if_several_have_no_priority(self):
        self.assertFalse(self.Source._get_by_database_type("interface"))

    def test_only_one_source_of_a_database_type_can_have_priority(self):
        self.sdb_live.set_priority()
        with self.assertRaises(ValidationError):
            self.sdb_test.priority = True
