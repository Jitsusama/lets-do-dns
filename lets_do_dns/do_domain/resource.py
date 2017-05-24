"""Performs lower level functions against DigitalOcean's REST API."""

import requests
from requests.exceptions import RequestException

from lets_do_dns.errors import RecordCreationError, RecordDeletionError
from lets_do_dns.do_domain.response import Response


class Resource(object):
    """Embody a DigitalOcean HTTP DNS Resource."""

    def __init__(self, record, value=None):
        self._record = record
        self.value = value
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
                self._uri, headers=self._header, **kwargs)
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
