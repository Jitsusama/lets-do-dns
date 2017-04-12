"""Test the acme_dns_authentication script."""

from requests import get, delete
from acmednsauth.authenticate import Authenticate


def test_digitalocean_authentication_record_creation(
        capsys, api_key, domain, fqdn, auth_token, temporary_filename,
        authorization_header, base_uri):
    # Emulate certbot passing in proper environment variables for
    # the authentication step.
    create_environment = {
        'DO_API_KEY': api_key,
        'DO_DOMAIN': domain,
        'CERTBOT_DOMAIN': fqdn,
        'CERTBOT_VALIDATION': auth_token,
    }

    # Exercise DNS authentication process.
    Authenticate(environment=create_environment)

    # Verify that the authentication process writes record id to STDOUT.
    record_id, _ = capsys.readouterr()
    assert int(record_id) > 0

    # Verify that the authentication process created the proper DNS record
    # with DigitalOcean.
    request_uri = '%s/%s/%d' % (base_uri, domain, record_id)
    response = get(request_uri, headers=authorization_header)
    record_data = response.json()['domain_record']
    assert record_data['type'] == 'TXT' and \
        record_data['name'] == fqdn and \
        record_data['data'] == auth_token

    # Manually cleanup the created DigitalOcean authentication DNS record.
    delete(request_uri, headers=authorization_header)
