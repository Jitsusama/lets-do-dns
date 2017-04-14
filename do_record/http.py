import requests

BASE_URI = 'https://api.digitalocean.com/v2/domains'


def create(record, value):
    """Create HTTP resource on DigitalOcean."""
    authorization_header = _authorization_header(record.api_key)
    post_uri = '%s/%s/%s' % (BASE_URI, record.domain, record.hostname)
    requests.post(post_uri, headers=authorization_header)
    return Response()


def _authorization_header(api_key):
    return {'Authorization': 'Bearer %s' % api_key}


class Response(object):
    """A response from DigitalOcean for making an HTTP resource request."""
    pass
