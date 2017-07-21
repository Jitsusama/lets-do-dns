"""Tests the lets_do_dns.acme_dns_auth.authenticate.py module."""

from mock import call, ANY
import pytest
from lets_do_dns.environment import Environment

from lets_do_dns.acme_dns_auth.authenticate import Authenticate


def test_properly_initializes_resource(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key='stub-api-key', domain='stub-domain', validation_key=None,
        fqdn='stub-host.stub-domain', record_id=984567, post_cmd=None)

    mock_resource = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Resource')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    mock_resource.assert_called_once_with(
        'stub-api-key', '_acme-challenge.stub-host',
        'stub-domain', None, 984567)


def test_triggers_resource_delete_after_resource_init(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key=None, domain='stub-domain', validation_key=None,
        fqdn='stub-host.stub-domain', record_id=0, post_cmd=None)

    mock_resource = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Resource')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    initialize_then_delete = [
        call(ANY, ANY, ANY, ANY, ANY),
        call().delete()]
    mock_resource.assert_has_calls(initialize_then_delete)


def test_does_not_call_sleep(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key=None, domain='stub-domain', validation_key=None,
        fqdn='stub-host.stub-domain', record_id=1, post_cmd=None)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Resource')

    mock_sleep = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.sleep')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    mock_sleep.assert_not_called()


@pytest.mark.parametrize(
    'fqdn', ['stub-host1.stub-domain', 'stub-host2.stub-domain'])
def test_passes_postcmd_to_run(mocker, fqdn):
    stub_environment = mocker.MagicMock(
        spec=Environment,
        api_key=None, domain='stub-domain', validation_key=None,
        fqdn=fqdn, record_id=3, post_cmd='test-program --help')
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Resource')

    mock_run = mocker.patch('lets_do_dns.acme_dns_auth.authenticate.run')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    mock_run.assert_called_once_with(
        'test-program --help',
        env={'CERTBOT_HOSTNAME': fqdn,
             'PATH': ["/bin", "/sbin",
                      "/usr/bin", "/usr/sbin",
                      "/usr/local/bin", "/usr/local/sbin"]})
