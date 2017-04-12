"""Test the DigitalOcean backed ACME DNS Authentication Class."""

from acmednsauth.authenticate import Authenticate
from mock import call
import pytest


@pytest.fixture()
def create_environment(api_key, domain, fqdn, auth_token):
    return {
        'DO_API_KEY': api_key,
        'DO_DOMAIN': domain,
        'CERTBOT_DOMAIN': fqdn,
        'CERTBOT_VALIDATION': auth_token,
    }


def test_valid_data_calls_record_creation_after_initialization(
        mocker, api_key, hostname, domain, auth_token, create_environment):
    record = mocker.patch('acmednsauth.authenticate.Record')

    Authenticate(environment=create_environment)

    initialize_then_create = [
        call(api_key, domain, hostname),
        call().create(auth_token)]
    record.assert_has_calls(initialize_then_create)


def test_valid_data_writes_to_printer_after_record_creation(
        mocker, create_environment):

    class FakeRecord(object):
        def __init__(self, a, b, c): pass
        def create(self, a): return 123456

    mocker.patch('acmednsauth.authenticate.Record', new=FakeRecord)
    stub_printer = mocker.patch('acmednsauth.authenticate.Printer')

    Authenticate(environment=create_environment)

    stub_printer.assert_has_calls([call(123456)])
