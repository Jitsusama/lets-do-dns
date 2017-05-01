from lets_do_dns.acme_dns_auth.authenticate import Authenticate

from lets_do_dns.environment import Environment

from mock import call

# ATTENTION: Look at conftest.py for py.test fixture definitions.


def test_triggers_record_creation_after_initialization(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment, domain='stub-domain', fqdn='create.stub-domain',
        api_key='stub-api-key', validation_key='stub-validation',
        record_id=None)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.sleep')

    mock_record = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Record')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    expected_txt_hostname = '_acme-challenge.create'
    initialize_then_create = [
        call('stub-api-key', 'stub-domain', expected_txt_hostname),
        call().create('stub-validation')]
    mock_record.assert_has_calls(initialize_then_create)


def test_pauses_after_successful_record_creation(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment, domain='stub-domain', fqdn='create.stub-domain',
        api_key=None, validation_key=None,
        record_id=None)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Record')

    stub_sleep = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.sleep')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    stub_sleep.assert_called_once_with(2)


def test_passes_record_id_to_printer_after_record_creation(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment, domain='stub-domain', fqdn='create.stub-domain',
        api_key=None, validation_key=None,
        record_id=None)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.sleep')

    stub_record = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Record')

    authentication = Authenticate(environment=stub_environment)
    authentication.perform()

    stub_record.assert_has_calls([call().printer()])


def test_returns_zero_after_successful_record_creation(mocker):
    stub_environment = mocker.MagicMock(
        spec=Environment, domain='stub-domain', fqdn='create.stub-domain',
        api_key=None, validation_key=None,
        record_id=None)
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.sleep')
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Record')

    authentication = Authenticate(environment=stub_environment)
    return_code = authentication.perform()

    assert return_code == 0
