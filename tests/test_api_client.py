import unittest
from unittest.mock import patch, Mock

from src.api_client import IpApiClient


class TestIpApiClient(unittest.TestCase):

    def setUp(self):
        """Prepare a sample API response before each test."""

        self.sample_data = {
            "success": True,
            "ip": "8.8.8.8",
            "country": "United States",
            "city": "Mountain View"
        }

    @patch("src.api_client.requests.get")
    def test_fetch_ip_data(self, mock_get):
        """Test that the API data is correctly retrieved."""

        mock_response = Mock()
        mock_response.json.return_value = self.sample_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = IpApiClient()
        result = client.fetch_ip_data()

        self.assertEqual(result["ip"], "8.8.8.8")
        self.assertEqual(result["country"], "United States")
        mock_get.assert_called_once()

    @patch("src.api_client.requests.get")
    def test_fetch_public_ip(self, mock_get):
        """Test that the public IP address is returned."""

        mock_response = Mock()
        mock_response.json.return_value = self.sample_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = IpApiClient()
        client.fetch_ip_data()

        self.assertEqual(client.fetch_public_ip(), "8.8.8.8")

    @patch("src.api_client.requests.get")
    def test_get_ip_version(self, mock_get):
        """Test that an IPv4 address is correctly identified."""

        mock_response = Mock()
        mock_response.json.return_value = self.sample_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = IpApiClient()
        client.fetch_ip_data()

        self.assertEqual(client.get_ip_version(), "IPv4")

    @patch("src.api_client.requests.get")
    def test_is_ipv6(self, mock_get):
        """Test that an IPv4 address is not identified as IPv6."""

        mock_response = Mock()
        mock_response.json.return_value = self.sample_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = IpApiClient()
        client.fetch_ip_data()

        self.assertFalse(client.is_ipv6())

    @patch("src.api_client.requests.get")
    def test_get_ip_data(self, mock_get):
        """Test that the complete API data can be accessed."""

        mock_response = Mock()
        mock_response.json.return_value = self.sample_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = IpApiClient()
        client.fetch_ip_data()

        result = client.get_ip_data()

        self.assertEqual(result["ip"], "8.8.8.8")
        self.assertEqual(result["city"], "Mountain View")

    @patch("src.api_client.requests.get")
    def test_api_connection_error(self, mock_get):
        """Test the handling of a connection error."""

        import requests

        mock_get.side_effect = requests.exceptions.ConnectionError(
            "Connection failed"
        )

        client = IpApiClient()

        with self.assertRaises(Exception):
            client.fetch_ip_data()

if __name__ == "__main__":
    unittest.main()
