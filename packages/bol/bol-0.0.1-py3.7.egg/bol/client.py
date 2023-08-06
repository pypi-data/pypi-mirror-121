"""
Core client functionality, common across all API requests.
"""

import requests
from urllib.parse import urlencode

_USER_AGENT = "BolApiClientPython/0.1"
_DEFAULT_BASE_URL = "https://api.bol.com/retailer"


class Client(object):
    """Performs requests to the Bol.com API."""


    def __init__(self, client_id, client_secret):
        """
        Base Bol.com api client.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()
        self._login()

    def _login(self):
        """
        Log in to the api by retrieving a Bearer token
        """
        print("logging in")

        self.session.headers.update({
            'User-Agent': _USER_AGENT,
            'Accept': 'application/json'
        })

        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }

        self.token = self.session.post(
            url = 'https://login.bol.com/token',
            data = payload
        ).json()['access_token']

        self.session.headers.update({
            'User-Agent': _USER_AGENT,
            'Accept': 'application/vnd.retailer.v3+json',
            'Authorization': 'Bearer ' + self.token
        })

    def _post(self, url, payload=None):
        """
        Performs HTTP GET/POST with credentials, returning the body as JSON.
        """

        response = self.session.post(url, data=payload)
        if response.status_code == 401:
            self._login()
            response = self.session.post(url, data=payload)
        return response.json()

    def _get(self, url, payload=None):
        """
        Performs HTTP GET/POST with credentials, returning the body as JSON.
        """

        response = self.session.get(url)
        if response.status_code == 401:
            self._login()
            response = self.session.get(url)
        return response.json()

    def _orders(self):
        """
        Fetch the open orders.
        """
        return self._get(_DEFAULT_BASE_URL + "/orders")

