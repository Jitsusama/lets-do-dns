from mock import call
import pytest

from lets_do_dns.acme_dns_auth.record import Record
from lets_do_dns.do_domain.resource import Resource


@pytest.mark.parametrize('input_record_id', [491834, 882342])
def test_create_stores_record_id_internally(mocker, input_record_id):
    mocker.patch('lets_do_dns.acme_dns_auth.dns.lookup')
    stub_int = mocker.patch(
        'lets_do_dns.acme_dns_auth.record.Resource.__int__',
        return_value=input_record_id)
    mocker.patch(
        'lets_do_dns.acme_dns_auth.record.Resource',
        spec=Resource, __int__=stub_int)

    record = Record(None, None, None)
    record.create(None)

    assert record.id == input_record_id


def test_create_properly_calls_http_create(mocker):
    mocker.patch(
        'lets_do_dns.acme_dns_auth.dns.lookup')

    mock_resource = mocker.patch(
        'lets_do_dns.acme_dns_auth.record.Resource')

    record = Record(None, None, None)
    record.create('dummy-auth-token')

    mock_resource.assert_has_calls([
        call(record, 'dummy-auth-token'),
        call().create()])


def test_create_properly_calls_exists_during_create(mocker):
    mocker.patch('lets_do_dns.acme_dns_auth.dns.lookup')
    mocker.patch('lets_do_dns.acme_dns_auth.record.Resource')

    mock_exists = mocker.patch.object(Record, 'exists')

    record = Record('stub-api-key', 'stub-domain', 'stub-hostname')
    record.create('dummy-auth-token')

    mock_exists.assert_called_once_with()


def test_delete_properly_calls_http_delete(mocker):
    mock_resource = mocker.patch(
        'lets_do_dns.acme_dns_auth.record.Resource')

    record = Record(None, None, None)
    record.delete()

    mock_resource.assert_has_calls([
        call(record),
        call().delete()])


def test_exists_properly_calls_lookup_during_create(mocker):
    mocker.patch(
        'lets_do_dns.acme_dns_auth.record.Resource')

    mock_lookup = mocker.patch(
        'lets_do_dns.acme_dns_auth.dns.lookup')

    record = Record('stub-api-key', 'stub-domain', 'stub-hostname')
    record.exists()

    mock_lookup.assert_called_once_with('stub-hostname.stub-domain')


def test_printer_calls_printer(mocker):
    mock_stdout = mocker.patch(
        'lets_do_dns.acme_dns_auth.record.stdout')
    record_id = 918342

    record = Record(None, None, None)
    record.id = record_id
    record.printer()

    mock_stdout.assert_called_once_with(record_id)
