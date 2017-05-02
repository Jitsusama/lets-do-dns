from mock import call
import pytest

from lets_do_dns.acme_dns_auth.record import Record


@pytest.mark.parametrize('input_record_id', [491834, 882342])
def test_create_stores_record_id_internally(mocker, input_record_id):
    mocker.patch(
        'lets_do_dns.acme_dns_auth.record.Resource.create')
    mocker.patch(
        'lets_do_dns.acme_dns_auth.record.Resource.__int__',
        return_value=input_record_id)

    record = Record(None, None, None)
    record.create(None)

    assert record.id == input_record_id


def test_create_properly_calls_http_create(mocker):
    stub_http_create = mocker.patch(
        'lets_do_dns.acme_dns_auth.record.Resource')

    record = Record(None, None, None)
    record.create('dummy-auth-token')

    stub_http_create.assert_has_calls([
        call(record, 'dummy-auth-token'),
        call().create()])


def test_delete_properly_calls_http_delete(mocker):
    stub_http_delete = mocker.patch(
        'lets_do_dns.acme_dns_auth.record.Resource')

    record = Record(None, None, None)
    record.delete()

    stub_http_delete.assert_has_calls([
        call(record),
        call().delete()])


def test_printer_calls_printer(mocker):
    stub_printer = mocker.patch(
        'lets_do_dns.acme_dns_auth.record.stdout')
    record_id = 918342

    record = Record(None, None, None)
    record.id = record_id
    record.printer()

    stub_printer.assert_called_once_with(record_id)
