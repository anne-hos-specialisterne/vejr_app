

# src/my_project/api_clients/base.py

import sys
import os

# Add the sibling folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from config.set_logging import setup_logger

logger = setup_logger(__name__)


class BaseAPIClient:
    def __init__(self, base_url, headers=None, timeout=10):
        """
        :param base_url: The root URL for the API
        :param headers: Dictionary of HTTP headers (optional)
        :param timeout: Timeout in seconds for requests
        """
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout
        self.session = requests.Session() #creates a requests session - has something to do with persistent HTTP and keeping the connection open
        self.session.headers.update(self.headers) # add headers to all requests fron the session

    def _request(self, method, endpoint, params=None, json=None):
        """
        Core request method.

        :param method: HTTP method as string ("GET", "POST", etc.)
        :param endpoint: API endpoint (e.g., "/weather")
        :param params: Dictionary of query parameters (optional)
        :param json: Dictionary for JSON body (optional)
        :return: Dictionary with API response
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                timeout=self.timeout,
            )
            response.raise_for_status()

            logger.info("API %s %s -> %s", method, url, response.status_code)

            if response.content:
                return response.json()
            return {}

        except requests.exceptions.RequestException as e:
            logger.error("API request failed: %s %s", method, url)
            raise e

    # Convenience methods
    def get(self, endpoint, params=None):
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint, json=None):
        return self._request("POST", endpoint, json=json)

    def put(self, endpoint, json=None):
        return self._request("PUT", endpoint, json=json)

    def delete(self, endpoint):
        return self._request("DELETE", endpoint)