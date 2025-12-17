from unittest.mock import MagicMock, patch

from odoo.tests import common


class TestIrUiViewUpdateFromSource(common.TransactionCase):
    def setUp(self):
        super().setUp()
        # Create a test view to work with
        self.test_view = self.env["ir.ui.view"].create(
            {
                "name": "test.view.example",
                "type": "qweb",
                "arch": "<div>Old content</div>",
            }
        )

        # Set the config parameter for the source URL
        self.env["ir.config_parameter"].set_param("snippet_manager.source_url", "https://odoo.build/snippets/")

    @patch("requests.get")
    def test_update_from_source_success(self, mock_get):
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<div>Updated content from source</div>"
        mock_get.return_value = mock_response

        # Call the method
        result = self.test_view.update_from_source()

        # Assertions
        mock_get.assert_called_once_with("https://odoo.build/snippets/test.view.example.xml", timeout=10)
        self.assertEqual(self.test_view.arch, "<div>Updated content from source</div>")
        self.assertEqual(result["result"], "updated")
        self.assertEqual(result["view_name"], "test.view.example")
        self.assertEqual(result["source"], "URL")

    @patch("requests.get")
    def test_update_from_source_http_error(self, mock_get):
        # Mock an HTTP error response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Ensure it raises an error
        with self.assertRaises(Exception) as context:
            self.test_view.update_from_source()

        self.assertIn("View definition for 'test.view.example' not found", str(context.exception))
        mock_get.assert_called_once_with("https://odoo.build/snippets/test.view.example.xml", timeout=10)

    @patch("requests.get")
    def test_update_from_source_request_exception(self, mock_get):
        # Mock a request exception
        mock_get.side_effect = Exception("Network error")

        # Ensure it raises an error
        with self.assertRaises(Exception) as context:
            self.test_view.update_from_source()

        self.assertIn("Unexpected error when fetching view", str(context.exception))
        mock_get.assert_called_once_with("https://odoo.build/snippets/test.view.example.xml", timeout=10)

    @patch("requests.get")
    def test_update_from_source_with_complex_xml(self, mock_get):
        # Mock response with more complex XML (Odoo removes XML declaration when storing)
        original_xml = """<?xml version="1.0"?>
<t>
    <div>
        <field name="test_field" readonly="1"/>
        <button name="action_test" type="object" string="Test Button"/>
    </div>
</t>"""

        # Expected value after Odoo processes it (without XML declaration)
        expected_arch = """<t>
    <div>
        <field name="test_field" readonly="1"/>
        <button name="action_test" type="object" string="Test Button"/>
    </div>
</t>"""

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = original_xml
        mock_get.return_value = mock_response

        # Call the method
        result = self.test_view.update_from_source()

        # Assertions
        mock_get.assert_called_once_with("https://odoo.build/snippets/test.view.example.xml", timeout=10)
        self.assertEqual(self.test_view.arch, expected_arch)
        self.assertEqual(result["result"], "updated")
        self.assertEqual(result["view_name"], "test.view.example")
