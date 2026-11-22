import requests
import ipaddress


class IpApiClient:
    """
    Client used to retrieve public IP address information
    from the ipapi.co REST API.
    """

    def __init__(self):
        self.__api_url = "https://ipwho.is/"
        self.__timeout = 10
        self.__ip_data = None

    def fetch_ip_data(self):
        """
        Sends an HTTP GET request to the API
        and returns the received JSON information.
        """
        try:
            response = requests.get(
                self.__api_url,
                timeout=self.__timeout
            )

            response.raise_for_status()

            data = response.json()

            if not isinstance(data, dict):
                raise ValueError("The API response is not a JSON object.")

            if data.get("success") is False:
                raise ValueError(
                    data.get("message", "The API returned an error.")
                )

            if data.get("error"):
                raise ValueError(
                    data.get("reason", "The API returned an error.")
                )

            ip_address = data.get("ip")

            if not ip_address:
                raise ValueError("The API response does not contain an IP address.")

            # Validate the returned IP address.
            ipaddress.ip_address(ip_address)

            self.__ip_data = data

            return data.copy()

        except requests.exceptions.Timeout:
            raise ConnectionError("The API request timed out.")

        except requests.exceptions.ConnectionError:
            raise ConnectionError("Unable to connect to the API.")

        except requests.exceptions.HTTPError as error:
            raise ConnectionError(f"HTTP error: {error}")

        except requests.exceptions.RequestException as error:
            raise ConnectionError(f"API request failed: {error}")

        except ValueError as error:
            raise ValueError(f"Invalid API response: {error}")

    def fetch_public_ip(self):
        """
        Returns the public IP address.
        Fetches the API information if it has not been retrieved yet.
        """
        if self.__ip_data is None:
            self.fetch_ip_data()

        return self.__ip_data["ip"]

    def get_ip_version(self):
        """
        Returns the IP version: IPv4 or IPv6.
        """
        if self.__ip_data is None:
            self.fetch_ip_data()

        address = ipaddress.ip_address(self.__ip_data["ip"])

        return f"IPv{address.version}"

    def is_ipv6(self):
        """
        Returns True if the public IP address is IPv6.
        Otherwise, returns False.
        """
        return self.get_ip_version() == "IPv6"

    def get_ip_data(self):
        """
        Returns a copy of the retrieved IP information.
        """
        if self.__ip_data is None:
            self.fetch_ip_data()

        return self.__ip_data.copy()
