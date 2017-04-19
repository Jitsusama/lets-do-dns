"""Performs lower level functions against DigitalOcean's REST API."""

import requests


class Resource(object):
    """Embody a DigitalOcean HTTP DNS Resource."""

    def __init__(self, record, value=None):
        self._record = record
        self.value = value
        self._response = None

    def create(self):
        """Post HTTP Resource to DigitalOcean."""
        self._response = Response(
            requests.post(
                self._uri, headers=self._header, json=self._json_data))

    def delete(self):
        """Delete HTTP Resource from DigitalOcean."""
        self._response = Response(
            requests.delete(
                self._uri, headers=self._header))

    def __int__(self):
        """Unique DigitalOcean identifier for this resource."""
        return self._response.resource_id

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


class Response(object):
    """HTTP resource request response from DigitalOcean."""

    def __init__(self, requests_response):
        self._response = requests_response
        self._check_response()

    @property
    def resource_id(self):
        """The resource identifier present in the DigitalOcean response."""
        if self._request_type != 'POST':
            return None

        json_response = self._response.json()

        return json_response['domain_record']['id']

    @property
    def _request_type(self):
        return self._response.request.method

    def _check_response(self):
        resource_request_failure = not self._response.ok

        if resource_request_failure:
            raise self._raise_creation_failure()

    def _raise_creation_failure(self):
        response_code = self._response.status_code
        resource_uri = self._response.url
        error_message = (
            'Encountered a %s response while creating the record resource '
            'at %s' % (response_code, resource_uri))

        return RecordCreationFailure(error_message)


class RecordCreationFailure(RuntimeError):
    """An error was encountered while attempting to create a record."""

    pass
