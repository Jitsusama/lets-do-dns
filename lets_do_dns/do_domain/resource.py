"""Performs lower level functions against DigitalOcean's REST API."""

import requests
from requests.exceptions import RequestException

from lets_do_dns.errors import AuthenticationFailure
from lets_do_dns.do_domain.response import Response


class Resource(object):
    """Embody a DigitalOcean HTTP DNS Resource."""

    def __init__(self, record, value=None):
        self._record = record
        self.value = value
        self._response = None

    def create(self):
        """Post HTTP Resource to DigitalOcean."""
        try:
            post_response = requests.post(
                self._uri, headers=self._header, json=self._json_data)
        except RequestException:
            raise AuthenticationFailure
        else:
            self._response = Response(post_response)

    def delete(self):
        """Delete HTTP Resource from DigitalOcean."""
        try:
            delete_response = requests.delete(
                self._uri, headers=self._header)
        except RequestException:
            raise AuthenticationFailure
        else:
            self._response = Response(delete_response)

    def __int__(self):
        """Unique DigitalOcean identifier for this resource."""
        return self._response.resource_id

    @property
    def _uri(self):
        common_uri = (
            'https://api.digitalocean.com/v2/domains/%s/records' % (
                self._record.domain))

        if self._record.id:
            return '%s/%s' % (common_uri, self._record.id)

        return common_uri

    @property
    def _header(self):
        return {'Authorization': 'Bearer %s' % self._record.api_key}

    @property
    def _json_data(self):
        return {'type': 'TXT',
                'name': self._record.hostname,
                'data': self.value}
