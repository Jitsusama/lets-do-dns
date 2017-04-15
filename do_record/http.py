import requests

BASE_URI = 'https://api.digitalocean.com/v2/domains'


def create(record, value):
    """Create HTTP resource on DigitalOcean."""
    authorization_header = _authorization_header(record.api_key)
    post_uri = _post_uri(record.domain, record.hostname)

    http_response = requests.post(post_uri, headers=authorization_header)

    return response(http_response)


def _post_uri(domain, hostname):
    return '%s/%s/%s' % (BASE_URI, domain, hostname)


def _authorization_header(api_key):
    return {'Authorization': 'Bearer %s' % api_key}


def response(requests_response):
    """A response from DigitalOcean for making an HTTP resource request."""
    resource_request_failure = not requests_response.ok

    if resource_request_failure:
        _raise_create_exception(requests_response)

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
