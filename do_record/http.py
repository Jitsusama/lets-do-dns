"""Performs lower level functions against DigitalOcean's REST API."""

import requests


class Resource(object):
    """Embody a DigitalOcean HTTP DNS Resource."""

    def __init__(self, record, value=None):
        self._record = record
        self.value = value
        self._request = None

    def create(self):
        """Post HTTP Resource to DigitalOcean."""
        self._request = requests.post(
            self._uri, headers=self._header, json=self._json_data)

    def delete(self):
        """Delete HTTP Resource from DigitalOcean."""
        self._request = requests.delete(
            self._uri, headers=self._header)

    def __int__(self):
        """Unique DigitalOcean identifier for this resource."""
        return response(self._request)

    @property
    def _uri(self):
        common_uri = (
            'https://api.digitalocean.com/v2/domains/%s/records' % (
                self._record.domain))

        if self._record.number:
            return '%s/%s' % (common_uri, self._record.number)

        return common_uri

    @property
    def _header(self):
        return {'Authorization': 'Bearer %s' % self._record.api_key}

    @property
    def _json_data(self):
        return {'type': 'TXT',
                'name': self._record.hostname,
                'data': self.value}


def response(requests_response):
    """A response from DigitalOcean for making an HTTP resource request."""
    resource_request_failure = not requests_response.ok

    if resource_request_failure:
        _raise_create_exception(requests_response)

    post_request = requests_response.request.method == 'POST'

    if post_request:
        return _grab_record_id(requests_response)


def _raise_create_exception(requests_response):
    response_code = requests_response.status_code
    resource_uri = requests_response.url
    error_message = (
        'Encountered a %s response while creating the record resource '
        'at %s' % (response_code, resource_uri))

    raise RecordCreationFailure(error_message)


def _grab_record_id(requests_response):
    json_response = requests_response.json()

    return json_response['domain_record']['id']


class RecordCreationFailure(RuntimeError):
    """An error was encountered while attempting to create a record."""

    pass
