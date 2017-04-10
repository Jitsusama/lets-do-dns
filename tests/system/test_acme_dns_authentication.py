"""Test the acme_dns_authentication script."""

import os
import pytest
from requests import get, delete
from acme_dns_auth.authenticate import Authenticate


BASE_URI = 'https://api.digitalocean.com/v2/domains'
API_KEY = str(
    'b7e303ba3771d024c0f1a62b9b8d1ad35d4c7db5a2a6ce69962618eb89a9276c')
DOMAIN = 'grrbrr.ca'
AUTHORIZATION_HEADER = {'Authorization': 'Bearer %s' % API_KEY}
AUTH_HOSTNAME = 'test-ssl-host.%s' % DOMAIN
AUTH_TOKEN = 'validate-with-this'
TEMPORARY_FILENAME = '/tmp/%s-%s' % (AUTH_HOSTNAME, AUTH_TOKEN)


def test_digitalocean_authentication_record_creation():
    # Setup
    create_environment = {
        'DO_API_KEY': API_KEY,
        'DO_DOMAIN': DOMAIN,
        'CERTBOT_DOMAIN': AUTH_HOSTNAME,
        'CERTBOT_VALIDATION': AUTH_TOKEN,
    }

    # Exercise
    Authenticate(environment=create_environment)
    temporary_file = open(TEMPORARY_FILENAME, 'r')
    record_id = int(temporary_file.read())

    # Assert
    response = get(request_uri(record_id), headers=AUTHORIZATION_HEADER)
    record_data = response.json()['domain_record']
    assert record_data['type'] == 'TXT' and \
        record_data['name'] == AUTH_HOSTNAME and \
        record_data['data'] == AUTH_TOKEN

    # Cleanup
    delete(request_uri(record_id), headers=AUTHORIZATION_HEADER)
    os.remove(TEMPORARY_FILENAME)


def request_uri(record_id):
    return '%s/%s/%d' % (BASE_URI, DOMAIN, record_id)
