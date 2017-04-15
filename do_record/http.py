import requests

BASE_URI = 'https://api.digitalocean.com/v2/domains'


def create(record, value):
    """Create HTTP resource on DigitalOcean."""
    authorization_header = _authorization_header(record.api_key)
    post_uri = '%s/%s/%s' % (BASE_URI, record.domain, record.hostname)
    http_response = requests.post(post_uri, headers=authorization_header)

    return response(http_response)


def _authorization_header(api_key):
    return {'Authorization': 'Bearer %s' % api_key}


def response(requests_response):
    """A response from DigitalOcean for making an HTTP resource request."""
    if not requests_response.ok:
        message = 'Encountered a %s response during record creation.' % (
            requests_response.status_code)
        raise RecordCreationFailure(message)

    return requests_response.json()['domain_record']['id']


class RecordCreationFailure(RuntimeError):
    """An error was encountered while attempting to create a record."""
    pass
