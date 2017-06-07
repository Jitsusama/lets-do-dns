"""Tests the lets_do_dns.acme_dns_auth.authenticate.py module."""

from mock import call, ANY
from lets_do_dns.environment import Environment
from lets_do_dns.do_domain.resource import Resource

from lets_do_dns.acme_dns_auth.authenticate import Authenticate


def test_properly_initializes_resource(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key='stub-api-key', domain='stub-domain',
        fqdn='stub-host.stub-domain', validation_key='stub-auth-key',
        post_cmd=None, record_id=None)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.lookup')
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.sleep')
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.stdout')

    mock_resource = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Resource')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    mock_resource.assert_called_with(
        'stub-api-key', '_acme-challenge.stub-host', 'stub-domain',
        'stub-auth-key', None)


def test_properly_calls_resource_create_after_resource_init(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key='stub-api-key', domain='stub-domain',
        fqdn='stub-host.stub-domain', validation_key='stub-validation',
        record_id=None)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.lookup')
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.sleep')
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.stdout')

    mock_resource = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Resource')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    initialize_then_create = [
        call(ANY, ANY, ANY, ANY, ANY),
        call().create()]
    mock_resource.assert_has_calls(initialize_then_create)


def test_properly_calls_dns_lookup(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key='stub-api-key', domain='stub-domain',
        fqdn='stub-host.stub-domain', validation_key='stub-validation',
        record_id=None)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.sleep')
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.stdout')
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Resource')

    mock_lookup = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.lookup')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    mock_lookup.assert_called_once_with(
        '_acme-challenge.stub-host.stub-domain')


def test_properly_calls_sleep(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key=None, domain='stub-domain',
        fqdn='stub-host.stub-domain', validation_key=None,
        record_id=None)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.lookup')
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.stdout')
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Resource')

    mock_sleep = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.sleep')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    mock_sleep.assert_called_once_with(2)


def test_passes_record_id_to_stdout(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key=None, domain='stub-domain',
        fqdn='stub-host.stub-domain', validation_key=None,
        record_id=None)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.lookup')
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.sleep')
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Resource',
                 spec=Resource, __int__=lambda _: 123567)

    mock_stdout = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.stdout')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    mock_stdout.assert_called_once_with(123567)
