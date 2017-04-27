"""Test the DigitalOcean backed ACME DNS Authentication Class."""

from lets_do_dns.acme_dns_auth.authenticate import Authenticate
from mock import call, PropertyMock


def test_triggers_record_deletion_after_initialization(
        mocker, do_api_key, do_domain, do_hostname, delete_environment):
    stub_record = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Record')
    txt_hostname = '%s.%s' % ('_acme-challenge', do_hostname)

    authentication = Authenticate(environment=delete_environment(0))
    authentication.perform()

    initialize_then_delete = [
        call(do_api_key, do_domain, txt_hostname),
        call().delete()]
    stub_record.assert_has_calls(initialize_then_delete)


def test_sets_record_number(mocker, delete_environment):
    mock_number = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Record.number',
        new_callable=PropertyMock)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Record.delete')
    record_id = 1235234

    authentication = Authenticate(
        environment=delete_environment(record_id))
    authentication.perform()

    assert mock_number.called_once_with(record_id)


def test_does_not_pause_after_record_deletion(
        mocker, delete_environment):
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Record')

    stub_sleep = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.sleep')

    authentication = Authenticate(environment=delete_environment(1))
    authentication.perform()

    stub_sleep.assert_not_called()


def test_runs_postcmd_program(mocker, delete_environment):
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Record')
    stub_run = mocker.patch('lets_do_dns.acme_dns_auth.authenticate.run')

    delete_environment = delete_environment(1)
    delete_environment.post_cmd = 'test-program --help'

    authentication = Authenticate(environment=delete_environment)
    authentication.perform()

    stub_run.assert_called_once_with('test-program --help')
