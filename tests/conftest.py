"""pytest shared testing configuration."""

import pytest


@pytest.fixture
def base_uri():
    return 'https://api.digitalocean.com/v2/domains'


@pytest.fixture
def api_key():
    return str(
        'b7e303ba3771d024c0f1a62b9b8d1ad35d4c7db5a2a6ce69962618eb89a9276c')


@pytest.fixture
def domain():
    return 'grrbrr.ca'


@pytest.fixture
def authorization_header(api_key):
    return {'Authorization': 'Bearer %s' % api_key}


@pytest.fixture
def hostname(domain):
    return 'test-ssl-host'


@pytest.fixture
def fqdn(hostname, domain):
    return '%s.%s' % (hostname, domain)


@pytest.fixture
def auth_token():
    return 'validate-with-this'


@pytest.fixture
def temporary_filename(fqdn, auth_token):
    return '/tmp/%s-%s' % (fqdn, auth_token)
