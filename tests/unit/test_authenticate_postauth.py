from lets_do_dns.acme_dns_auth.authenticate import Authenticate

from lets_do_dns.environment import Environment
from lets_do_dns.acme_dns_auth.record import Record

from mock import call

# ATTENTION: Look at conftest.py for py.test fixture definitions.


def test_triggers_record_deletion_after_initialization(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment, api_key='test-key', domain='grrbrr.ca',
        record_id=0, fqdn='test-host.grrbrr.ca', post_cmd=None)

    mock_record = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Record')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    expected_challenge_hostname = '_acme-challenge.test-host'
    initialize_then_delete = [
        call('test-key', 'grrbrr.ca', expected_challenge_hostname),
        call().delete()]
    mock_record.assert_has_calls(initialize_then_delete)


def test_sets_record_number(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment, domain='grrbrr.ca', fqdn='testing.grrbrr.ca',
        record_id=1235234, api_key=None, post_cmd=None)

    mock_record = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Record', spec=Record)

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    assert mock_record.return_value.id == 1235234


def test_does_not_pause_after_record_deletion(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment, domain='grrbrr.ca', fqdn='b.grrbrr.ca',
        record_id=1, api_key=None, post_cmd=None)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Record')

    stub_sleep = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.sleep')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    stub_sleep.assert_not_called()


def test_runs_postcmd_program(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment, domain='grrbrr.ca', fqdn='c.grrbrr.ca',
        record_id=3, api_key=None, post_cmd='test-program --help')
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Record')

    mock_run = mocker.patch('lets_do_dns.acme_dns_auth.authenticate.run')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    mock_run.assert_called_once_with('test-program --help')
