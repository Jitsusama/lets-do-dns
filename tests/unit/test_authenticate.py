"""Test the DigitalOcean backed ACME DNS Authentication Class."""

from acmednsauth.authenticate import Authenticate
from mock import call

API_KEY = 'super-secret-key'
AUTHORIZATION_HEADER = {'Authorization': 'Bearer %s' % API_KEY}
AUTH_TOKEN = 'validate-with-this'
DOMAIN = 'grrbrr.ca'
HOSTNAME = 'testing-ssl-host'

CREATE_ENVIRONMENT = {
   'DO_API_KEY': API_KEY,
   'DO_DOMAIN': DOMAIN,
   'CERTBOT_DOMAIN': '%s.%s' % (HOSTNAME, DOMAIN),
   'CERTBOT_VALIDATION': AUTH_TOKEN
}


def test_triggering_of_record_creation_after_initialization(mocker):
    mocker.patch('acmednsauth.authenticate.printer')
    record = mocker.patch('acmednsauth.authenticate.Record')

    Authenticate(environment=CREATE_ENVIRONMENT)

    initialize_then_create = [
        call(API_KEY, DOMAIN, HOSTNAME),
        call().create(AUTH_TOKEN)]
    record.assert_has_calls(initialize_then_create)


class FakeRecord(object):
    def __init__(self, a, b, c): pass

    @staticmethod
    def create(_): return 123456


def test_passes_record_id_to_printer_after_record_creation(mocker):
    mocker.patch('acmednsauth.authenticate.Record', new=FakeRecord)
    stub_printer = mocker.patch('acmednsauth.authenticate.printer')

    Authenticate(environment=CREATE_ENVIRONMENT)

    stub_printer.assert_called_once_with(123456)
