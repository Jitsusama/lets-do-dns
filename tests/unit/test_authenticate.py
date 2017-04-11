"""Test the DigitalOcean backed ACME DNS Authentication Class."""

from acmednsauth.authenticate import Authenticate
from mock import call


def test_valid_data_calls_digital_ocean_record_creation(
        mocker, api_key, hostname, domain, fqdn, auth_token):
    create_environment = {
        'DO_API_KEY': api_key,
        'DO_DOMAIN': domain,
        'CERTBOT_DOMAIN': fqdn,
        'CERTBOT_VALIDATION': auth_token,
    }

    record = mocker.patch('acmednsauth.authenticate.Record')

    Authenticate(environment=create_environment)

    record.assert_called_once_with(api_key, domain, hostname)
    record.has_calls([call().create(auth_token)])
