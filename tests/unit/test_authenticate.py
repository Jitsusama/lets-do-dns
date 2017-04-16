"""Test the DigitalOcean backed ACME DNS Authentication Class."""

from certbot_dns_auth import Authenticate
from mock import call


def test_triggering_of_record_creation_after_initialization(
        mocker, env, create_environment):
    mocker.patch('certbot_dns_auth.authenticate.printer')
    stub_record = mocker.patch('certbot_dns_auth.authenticate.Record')

    Authenticate(environment=create_environment)

    initialize_then_create = [
        call(env.key, env.domain, env.hostname),
        call().create(env.auth_token)]
    stub_record.assert_has_calls(initialize_then_create)


def test_passes_record_id_to_printer_after_record_creation(
        mocker, create_environment, fake_record):
    mocker.patch('certbot_dns_auth.authenticate.Record', new=fake_record)
    stub_printer = mocker.patch('certbot_dns_auth.authenticate.printer')

    Authenticate(environment=create_environment)

    stub_printer.assert_called_once_with(123456)
