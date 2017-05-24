"""HTTP RESTful API Responses From DigitalOcean."""

from lets_do_dns.errors import RecordCreationError, RecordDeletionError

from requests.exceptions import HTTPError


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
        try:
            self._response.raise_for_status()
        except HTTPError as exception:
            if self._request_type == 'POST':
                raise RecordCreationError(exception)
            else:
                raise RecordDeletionError(exception)
