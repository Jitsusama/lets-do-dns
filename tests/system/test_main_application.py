"""Test the acme_dns_authentication script."""

from requests import get, delete
from acmednsauth.authenticate import Authenticate


def test_digitalocean_authentication_record_creation(capsys, env):
    # Emulate certbot passing in proper environment variables for
    # the authentication step.
    create_environment = {
        'DO_API_KEY': env.key,
        'DO_DOMAIN': env.domain,
        'CERTBOT_DOMAIN': '%s.%s' % (env.hostname, env.domain),
        'CERTBOT_VALIDATION': env.auth_token,
    }

    # Exercise DNS authentication process.
    Authenticate(environment=create_environment)

    # Verify that the authentication process writes record id to STDOUT.
    record_id, _ = capsys.readouterr()
    assert int(record_id) > 0

    # Verify that the authentication process created the proper DNS record
    # with DigitalOcean.
    request_uri = '%s/%s/%s' % (env.base_uri, env.domain, record_id)
    response = get(request_uri, headers=env.auth_header)
    record_data = response.json()['domain_record']
    assert record_data['type'] == 'TXT' and \
        record_data['name'] == '%s.%s' % (env.hostname, env.domain) and \
        record_data['data'] == env.auth_token

    # Manually cleanup the created DigitalOcean authentication DNS record.
    delete(request_uri, headers=env.auth_header)
