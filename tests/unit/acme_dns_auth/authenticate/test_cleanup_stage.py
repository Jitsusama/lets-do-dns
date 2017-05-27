"""Tests the lets_do_dns.acme_dns_auth.authenticate.py module."""

from mock import call, ANY
from lets_do_dns.environment import Environment
from lets_do_dns.acme_dns_auth.record import Record

from lets_do_dns.acme_dns_auth.authenticate import Authenticate


def test_properly_initializes_record(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key='stub-api-key', domain='stub-domain',
        fqdn='stub-host.stub-domain', record_id=0, post_cmd=None)

    mock_record = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Record')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    mock_record.assert_called_with(
        'stub-api-key', 'stub-domain', '_acme-challenge.stub-host')


def test_triggers_record_delete_after_record_init(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key=None, domain='stub-domain',
        fqdn='stub-host.stub-domain', record_id=0, post_cmd=None)

    mock_record = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Record')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    initialize_then_delete = [
        call(ANY, ANY, ANY),
        call().delete()]
    mock_record.assert_has_calls(initialize_then_delete)


def test_sets_record_number(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key=None, domain='stub-domain',
        fqdn='stub-host.stub-domain', record_id=12352, post_cmd=None)

    mock_record = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Record', spec=Record)

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    assert mock_record.return_value.id == 12352


def test_does_not_call_sleep(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key=None, domain='stub-domain',
        fqdn='stub-host.stub-domain', record_id=1, post_cmd=None)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Record')

    mock_sleep = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.sleep')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    mock_sleep.assert_not_called()


def test_passes_postcmd_to_run(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key=None, domain='stub-domain',
        fqdn='stub-host.stub-domain', record_id=3,
        post_cmd='test-program --help')
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Record')

    mock_run = mocker.patch('lets_do_dns.acme_dns_auth.authenticate.run')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    mock_run.assert_called_once_with('test-program --help')
