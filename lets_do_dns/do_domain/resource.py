"""Performs lower level functions against DigitalOcean's REST API."""

import requests
from requests.exceptions import RequestException

from lets_do_dns.errors import RecordCreationError, RecordDeletionError
from lets_do_dns.do_domain.response import Response


class Resource(object):
    """Embody a DigitalOcean HTTP DNS Resource."""

    def __init__(
            self, api_key, hostname, domain, value=None, record_id=None):
        self.api_key = api_key
        self.hostname = hostname
        self.domain = domain
        self.value = value
        self.record_id = record_id
        self._response = None

    def create(self):
        """Post HTTP Resource to DigitalOcean."""
        self._perform_http_operation(
            requests.post, json=self._json_data)

    def delete(self):
        """Delete HTTP Resource from DigitalOcean."""
        self._perform_http_operation(
            requests.delete)

    def _perform_http_operation(self, requests_operation, **kwargs):
        try:
            response = requests_operation(
                self._uri, headers=self._header,
                timeout=self._http_timeout, **kwargs)
        except RequestException as exception:
            if requests_operation is requests.post:
                raise RecordCreationError(exception)
            else:
                raise RecordDeletionError(exception)
        else:
            self._response = Response(response)

    def __int__(self):
        """Unique DigitalOcean identifier for this resource."""
        return self._response.resource_id

    @property
    def _uri(self):
        common_uri = (
            'https://api.digitalocean.com/v2/domains'
            '/%s/records' % self.domain)

        if self.record_id:
            return '%s/%s' % (common_uri, self.record_id)

        return common_uri

    @property
    def _header(self):
        return {'Authorization': 'Bearer %s' % self.api_key}

    @property
    def _json_data(self):
        return {'type': 'TXT',
                'name': self.hostname,
                'data': self.value}

    @property
    def _http_timeout(self):
        tcp_connection_timeout = 10
        http_data_timeout = 10

        return tcp_connection_timeout, http_data_timeout
