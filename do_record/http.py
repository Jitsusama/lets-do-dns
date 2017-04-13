import requests

BASE_URI = 'https://api.digitalocean.com/v2/domains'


def create(record, value):
    """Create HTTP resource on DigitalOcean."""
    requests.put('%s/%s/%s' % (BASE_URI, record.domain, record.hostname))
