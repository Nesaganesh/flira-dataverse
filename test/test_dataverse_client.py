import unittest
from unittest.mock import Mock, patch

from src.dataverse_client import DataverseApi, DataverseClient


class DataverseClientTests(unittest.TestCase):
    @patch("dataverse_client.requests.post")
    def test_get_access_token_returns_token(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"access_token": "abc123"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        client = DataverseClient(
            tenant_id="tenant",
            client_id="client",
            client_secret="secret",
            dataverse_url="https://example.crm.dynamics.com",
        )

        self.assertEqual(client.get_access_token(), "abc123")
        self.assertEqual(
            client.headers["Authorization"],
            "Bearer abc123",
        )

    def test_headers_include_required_values(self):
        client = DataverseClient(
            tenant_id="tenant",
            client_id="client",
            client_secret="secret",
            dataverse_url="https://example.crm.dynamics.com",
            token="demo-token",
        )

        self.assertEqual(
            client.get_headers()["Authorization"],
            "Bearer demo-token",
        )
        self.assertEqual(client.get_headers()["Accept"], "application/json")

    @patch("dataverse_client.requests.request")
    def test_api_wrapper_methods_use_generic_calls(self, mock_request):
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {"value": []}
        mock_request.return_value = mock_response

        client = DataverseClient(
            tenant_id="tenant",
            client_id="client",
            client_secret="secret",
            dataverse_url="https://example.crm.dynamics.com",
            token="demo-token",
        )
        api = DataverseApi(client)

        api.create_property({"flira_name": "Test"})
        api.get_property_metadata()
        api.get_property_columns()

        self.assertEqual(mock_request.call_count, 3)


if __name__ == "__main__":
    unittest.main()
