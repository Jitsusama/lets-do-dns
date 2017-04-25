"""Test the DigitalOcean backed ACME DNS Authentication Class."""

from lets_do_dns.acme_dns_auth.authenticate import Authenticate
from mock import call


def test_triggers_record_creation_after_initialization(
        mocker, env, create_environment):
    stub_record = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Record')

    authentication = Authenticate(environment=create_environment)
    authentication.perform()

    initialize_then_create = [
        call(env.key, env.domain, env.hostname),
        call().create(env.auth_token)]
    stub_record.assert_has_calls(initialize_then_create)


def test_passes_record_id_to_printer_after_record_creation(
        mocker, create_environment):
    stub_record = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Record')

    authentication = Authenticate(environment=create_environment)
    authentication.perform()

    stub_record.assert_has_calls([call().printer()])


def test_returns_zero_after_successful_record_creation(
        mocker, create_environment):
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Record')

    authentication = Authenticate(environment=create_environment)
    return_code = authentication.perform()

    assert return_code == 0
