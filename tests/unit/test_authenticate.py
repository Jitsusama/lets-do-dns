"""Test the DigitalOcean backed ACME DNS Authentication Class."""

from acmednsauth.authenticate import Authenticate
from mock import call, ANY


def test_valid_data_calls_record_creation_after_initialization(
        mocker, api_key, hostname, domain, fqdn, auth_token):
    create_environment = {
        'DO_API_KEY': api_key,
        'DO_DOMAIN': domain,
        'CERTBOT_DOMAIN': fqdn,
        'CERTBOT_VALIDATION': auth_token,
    }

    record = mocker.patch('acmednsauth.authenticate.Record')

    Authenticate(environment=create_environment)

    initialize_then_create = [
        call(api_key, domain, hostname),
        call().create(auth_token)]
    record.assert_has_calls(initialize_then_create)
