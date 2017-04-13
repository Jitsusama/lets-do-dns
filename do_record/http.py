import requests

BASE_URI = 'https://api.digitalocean.com/v2/domains'


def create(api_key, domain, hostname, value):
    """Create HTTP resource on DigitalOcean."""
    requests.put('%s/%s/%s' % (BASE_URI, domain, hostname))
