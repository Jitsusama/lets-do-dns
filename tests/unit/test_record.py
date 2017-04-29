import pytest
from mock import call

from lets_do_dns.acme_dns_auth.record import Record


# ATTENTION: Look at conftest.py for py.test fixture definitions.


@pytest.mark.parametrize('input_record_id', [491834, 882342])
def test_create_stores_record_id_internally(
        mocker, do_api_key, do_domain, do_hostname, certbot_auth_token,
        input_record_id):
    mocker.patch(
        'lets_do_dns.acme_dns_auth.record.Resource.create')
    mocker.patch(
        'lets_do_dns.acme_dns_auth.record.Resource.__int__',
        return_value=input_record_id)

    record = Record(do_api_key, do_domain, do_hostname)
    record.create(certbot_auth_token)

    assert record.id == input_record_id


def test_create_properly_calls_http_create(
        mocker, do_api_key, do_domain, do_hostname, certbot_auth_token):
    stub_http_create = mocker.patch(
        'lets_do_dns.acme_dns_auth.record.Resource')

    record = Record(do_api_key, do_domain, do_hostname)
    record.create(certbot_auth_token)

    stub_http_create.assert_has_calls([
        call(record, certbot_auth_token),
        call().create()])


@pytest.mark.parametrize('record_id', [491834])
def test_delete_properly_calls_http_delete(
        mocker, do_api_key, do_domain, do_hostname, record_id):
    stub_http_delete = mocker.patch(
        'lets_do_dns.acme_dns_auth.record.Resource')

    record = Record(do_api_key, do_domain, do_hostname)
    record.id = record_id
    record.delete()

    stub_http_delete.assert_has_calls([
        call(record),
        call().delete()])


def test_printer_calls_printer(mocker, do_api_key, do_domain, do_hostname):
    stub_printer = mocker.patch(
        'lets_do_dns.acme_dns_auth.record.stdout')
    record_id = 918342

    record = Record(do_api_key, do_domain, do_hostname)
    record.id = record_id
    record.printer()

    stub_printer.assert_called_once_with(record_id)
