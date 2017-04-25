"""HTTP RESTful API Responses From DigitalOcean."""

from lets_do_dns.do_domain.errors import RecordCreationFailure


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
