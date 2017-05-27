"""Tests the lets_do_dns.acme_dns_auth.record.py module."""

from mock import call
import pytest
from lets_do_dns.do_domain.resource import Resource

from lets_do_dns.acme_dns_auth.record import Record


@pytest.mark.parametrize('expected_record_id', [491834, 882342])
def test_create_stores_record_id_internally(mocker, expected_record_id):
    mocker.patch('lets_do_dns.dns_tools.lookup.lookup')
    stub_int = mocker.patch(
        'lets_do_dns.acme_dns_auth.record.Resource.__int__',
        return_value=expected_record_id)
    mocker.patch(
        'lets_do_dns.acme_dns_auth.record.Resource',
        spec=Resource, __int__=stub_int)

    record = Record(None, None, None)
    record.create(None)

    assert record.id == expected_record_id


def test_create_properly_calls_http_create(mocker):
    mocker.patch('lets_do_dns.dns_tools.lookup.lookup')

    mock_resource = mocker.patch(
        'lets_do_dns.acme_dns_auth.record.Resource')

    record = Record(None, None, None)
    record.create('dummy-auth-token')

    mock_resource.assert_has_calls([
        call(record, 'dummy-auth-token'),
        call().create()])


def test_delete_properly_calls_http_delete(mocker):
    mock_resource = mocker.patch(
        'lets_do_dns.acme_dns_auth.record.Resource')

    record = Record(None, None, None)
    record.delete()

    mock_resource.assert_has_calls([
        call(record),
        call().delete()])


def test_exists_properly_calls_lookup(mocker):
    mocker.patch('lets_do_dns.acme_dns_auth.record.Resource')

    mock_lookup = mocker.patch(
        'lets_do_dns.dns_tools.lookup.lookup')

    record = Record('stub-api-key', 'stub-domain', 'stub-host')
    record.exists()

    mock_lookup.assert_called_once_with('stub-host.stub-domain')


def test_printer_calls_printer(mocker):
    mock_stdout = mocker.patch(
        'lets_do_dns.acme_dns_auth.record.stdout')
    record_id = 918342

    record = Record(None, None, None)
    record.id = record_id
    record.printer()

    mock_stdout.assert_called_once_with(record_id)
