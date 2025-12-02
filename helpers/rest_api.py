# File: helpers/reset_api.py
import requests


class RestApi:
    def __init__(self, url, access_token=None):
        self.url = url
        self.access_token = access_token

    def _generate_headers(self, **kwargs):
        headers = kwargs.get('headers', {})
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    def get(self, **kwargs):
        headers = self._generate_headers(**kwargs)
        return requests.get(self.url, headers=headers, timeout=5)

    def delete(self, **kwargs):
        headers = self._generate_headers(**kwargs)
        return requests.delete(self.url, headers=headers, timeout=5)

    def post(self, **kwargs):
        headers = self._generate_headers(**kwargs)
        return requests.post(self.url, headers=headers, timeout=5, **kwargs)

    def patch(self, **kwargs):
        headers = self._generate_headers(**kwargs)
        return requests.patch(self.url, headers=headers, timeout=5, **kwargs)