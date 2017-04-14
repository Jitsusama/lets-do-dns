"""Test the acme_dns_authentication script."""

from requests import get, delete
from acmednsauth.authenticate import Authenticate

API_KEY = (
    'b7e303ba3771d024c0f1a62b9b8d1ad35d4c7db5a2a6ce69962618eb89a9276c')
AUTHORIZATION_HEADER = {'Authorization': 'Bearer %s' % API_KEY}
AUTH_TOKEN = 'validate-with-thing'
BASE_URI = 'https://api.digitalocean.com/v2/domains'
DOMAIN = 'grrbrr.ca'
HOSTNAME = 'test-ssl-host'


def test_digitalocean_authentication_record_creation(
        capsys, authorization_header):
    # Emulate certbot passing in proper environment variables for
    # the authentication step.
    create_environment = {
        'DO_API_KEY': API_KEY,
        'DO_DOMAIN': DOMAIN,
        'CERTBOT_DOMAIN': '%s.%s' % (HOSTNAME, DOMAIN),
        'CERTBOT_VALIDATION': AUTH_TOKEN,
    }

    # Exercise DNS authentication process.
    Authenticate(environment=create_environment)

    # Verify that the authentication process writes record id to STDOUT.
    record_id, _ = capsys.readouterr()
    assert int(record_id) > 0

    # Verify that the authentication process created the proper DNS record
    # with DigitalOcean.
    request_uri = '%s/%s/%s' % (BASE_URI, DOMAIN, record_id)
    response = get(request_uri, headers=AUTHORIZATION_HEADER)
    record_data = response.json()['domain_record']
    assert record_data['type'] == 'TXT' and \
        record_data['name'] == '%s.%s' % (HOSTNAME, DOMAIN) and \
        record_data['data'] == AUTH_TOKEN

    # Manually cleanup the created DigitalOcean authentication DNS record.
    delete(request_uri, headers=authorization_header)
