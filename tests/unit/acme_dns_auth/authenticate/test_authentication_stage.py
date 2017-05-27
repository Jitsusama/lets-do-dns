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


def test_properly_calls_record_create_after_record_init(mocker):
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


def test_calls_record_exists_after_record_create(mocker):
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
        call().create(ANY),
        call().exists()]
    mock_record.assert_has_calls(initialize_then_create)


def test_properly_calls_sleep(mocker):
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


def test_passes_record_id_to_printer(mocker):
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
