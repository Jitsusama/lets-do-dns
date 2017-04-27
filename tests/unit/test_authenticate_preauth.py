from lets_do_dns.acme_dns_auth.authenticate import Authenticate
from mock import call

# ATTENTION: Look at conftest.py for py.test fixture definitions.


def test_triggers_record_creation_after_initialization(
        mocker, do_api_key, do_domain, do_hostname, certbot_auth_token,
        create_environment):
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.sleep')

    stub_record = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Record')
    txt_hostname = '%s.%s' % ('_acme-challenge', do_hostname)

    authentication = Authenticate(environment=create_environment)
    authentication.perform()

    initialize_then_create = [
        call(do_api_key, do_domain, txt_hostname),
        call().create(certbot_auth_token)]
    stub_record.assert_has_calls(initialize_then_create)


def test_pauses_after_successful_record_creation(
        mocker, create_environment):
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Record')

    stub_sleep = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.sleep')

    authentication = Authenticate(environment=create_environment)
    authentication.perform()

    stub_sleep.assert_called_once_with(2)


def test_passes_record_id_to_printer_after_record_creation(
        mocker, create_environment):
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.sleep')

    stub_record = mocker.patch(
        'lets_do_dns.acme_dns_auth.authenticate.Record')

    authentication = Authenticate(environment=create_environment)
    authentication.perform()

    stub_record.assert_has_calls([call().printer()])


def test_returns_zero_after_successful_record_creation(
        mocker, create_environment):
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.sleep')
    mocker.patch('lets_do_dns.acme_dns_auth.authenticate.Record')

    authentication = Authenticate(environment=create_environment)
    return_code = authentication.perform()

    assert return_code == 0
