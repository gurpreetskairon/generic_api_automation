"""
api_context.py
---------------
This module defines the `APIContext` class, which wraps Playwright’s `RequestContext`
to simplify REST API testing. It provides helper methods for making HTTP requests,
parsing JSON and XML responses, and verifying status codes or response content.

Author: [Your Name]
Date: [Date]
"""
from typing import overload

from playwright.sync_api import sync_playwright
import xml.etree.ElementTree as ET
import re
from typing import Optional


class APIContext:
    """
    A lightweight API testing utility built on top of Playwright’s request context.

    Attributes
    ----------
    request : object
        Playwright request context instance.
    base_url : str
        Base URL for API requests.
    endpoint : str
        Specific endpoint to append to the base URL.
    query_params : dict
        URL query parameters for GET requests.
    request_body : dict
        Request body for POST/PUT requests.
    headers : dict
        HTTP headers to include in the request.
    auth_token : str, optional
        Bearer token for authentication (if applicable).
    basic_auth : tuple, optional
        (username, password) tuple for basic authentication.
    response : object
        Playwright response object (set after request is made).
    """

    def __init__(self, request_context):
        """Initializes the API context with a given Playwright request context."""
        self.request = request_context
        self.base_url = ""
        self.endpoint = ""
        self.query_params = {}
        self.request_body = {}
        self.headers = {}
        self.auth_token = None
        self.basic_auth = None
        self.method="get"
        self.response = None

    # --------------------------------------------------------------------------
    # Core HTTP methods
    # --------------------------------------------------------------------------

    def get(self):
        """Sends a GET request using the configured base URL, endpoint, and headers."""
        self.response = self.request.get(
            url=f"{self.base_url}{self.endpoint}",
            headers=self.headers,
            params=self.query_params,
        )

    def post(self):
        """Sends a POST request with the configured URL, headers, and body."""
        self.response = self.request.post(
            url=f"{self.base_url}{self.endpoint}",
            data=self.request_body,
            headers=self.headers,
        )

    def put(self):
        """Sends a PUT request with the configured URL, headers, and body."""
        self.response = self.request.put(
            url=f"{self.base_url}{self.endpoint}",
            data=self.request_body,
            headers=self.headers,
        )

    def delete(self):
        """Sends a DELETE request with the configured URL and headers."""
        self.response = self.request.delete(
            url=f"{self.base_url}{self.endpoint}",
            headers=self.headers,
            params=self.query_params,
        )

    # --------------------------------------------------------------------------
    # Request dispatcher
    # --------------------------------------------------------------------------
    def send_request(self, method: Optional[str] = None):
        """
        Sends an HTTP request based on the given method, or the instance's preset method if not provided.

        Parameters
        ----------
        method : str, optional
            HTTP method to use (GET, POST, etc.). Defaults to self.method if not provided.
        """
        method = method or self.method

        if method.lower() == "get":
            self.get()
        elif method.lower() == "post":
            self.post()
        elif method.lower() == "put":
            self.put()
        elif method.lower() == "delete":
            self.delete()
        else:
            raise ValueError(f"Unsupported HTTP method: {method.lower()}")


    # --------------------------------------------------------------------------
    # Response helpers
    # --------------------------------------------------------------------------

    def get_response_json(self):
        """Returns the JSON-parsed response body."""
        if not self.response:
            raise Exception("No response available.")
        return self.response.json()

    def get_status_code(self):
        """Returns the HTTP status code of the last response."""
        if not self.response:
            raise Exception("No response available.")
        return self.response.status

    def verify_response_status(self, expected_status_code: int):
        """
        Asserts that the response status code matches the expected code.

        Parameters
        ----------
        expected_status_code : int
            The expected HTTP status code.
        """
        if not self.response:
            raise Exception("No response available for verification.")
        assert self.response.status == int(expected_status_code), (
            f"Expected {expected_status_code}, but got {self.response.status}"
        )



