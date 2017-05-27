"""Tests the lets_do_dns.acme_dns_auth.authenticate.py module."""

from mock import call, ANY
from lets_do_dns.environment import Environment

from lets_do_dns.acme_dns_auth.authenticate import Authenticate


def test_properly_initializes_record(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key='stub-api-key', domain='stub-domain',
        fqdn='stub-host.stub-domain', validation_key=None,
        post_cmd=None, record_id=None)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.sleep')

    mock_record = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Record')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    mock_record.assert_called_with(
        'stub-api-key', 'stub-domain', '_acme-challenge.stub-host')


def test_triggers_record_creation_after_initialization(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key='stub-api-key', domain='stub-domain',
        fqdn='stub-host.stub-domain', validation_key='stub-validation',
        record_id=None)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.sleep')

    mock_record = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Record')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    initialize_then_create = [
        call(ANY, ANY, ANY),
        call().create('stub-validation')]
    mock_record.assert_has_calls(initialize_then_create)


def test_calls_exists_on_record_after_creation(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key='stub-api-key', domain='stub-domain',
        fqdn='stub-host.stub-domain', validation_key='stub-validation',
        record_id=None)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.sleep')

    mock_record = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Record')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    initialize_then_create = [
        call().create('stub-validation'),
        call().exists()]
    mock_record.assert_has_calls(initialize_then_create)


def test_pauses_after_successful_record_creation(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key=None, domain='stub-domain',
        fqdn='stub-host.stub-domain', validation_key=None,
        record_id=None)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Record')

    mock_sleep = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.sleep')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    mock_sleep.assert_called_once_with(2)


def test_passes_record_id_to_printer_after_record_creation(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key=None, domain='stub-domain',
        fqdn='stub-host.stub-domain', validation_key=None,
        record_id=None)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.sleep')

    mock_record = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Record')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    mock_record.assert_has_calls([call().printer()])


def test_returns_zero_after_successful_record_creation(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key=None, domain='stub-domain',
        fqdn='stub-host.stub-domain', validation_key=None,
        record_id=None)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.sleep')
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Record')

    authentication = Authenticate(environment=stub_environment)
    return_code = authentication.perform()

    assert return_code == 0
