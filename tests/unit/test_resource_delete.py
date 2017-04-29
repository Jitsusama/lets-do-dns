import pytest
from mock import ANY

from lets_do_dns.do_domain.resource import Resource
from lets_do_dns.acme_dns_auth.record import Record

# ATTENTION: Look at conftest.py for py.test fixture definitions.


def test_calls_delete(mocker):
    stub_record = mocker.MagicMock(
        spec=Record, api_key=None, domain=None, id=None)

    mock_requests = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete')

    resource = Resource(stub_record)
    resource.delete()

    mock_requests.assert_called_once()


@pytest.mark.parametrize('record_id', [82227342, 2342552])
def test_calls_correct_uri(mocker, record_id, do_domain):
    stub_record = mocker.MagicMock(
        spec=Record, api_key=None, domain=None, id=None)
    stub_record.domain = do_domain
    stub_record.id = record_id

    mock_requests = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete')

    resource = Resource(stub_record)
    resource.delete()

    record_delete_uri = (
        'https://api.digitalocean.com/v2/domains/%s/records/%s' % (
            do_domain, record_id))

    mock_requests.assert_called_once_with(record_delete_uri, headers=ANY)


def test_passes_authorization_header(mocker, do_auth_header, do_api_key):
    stub_record = mocker.MagicMock(
        spec=Record, api_key=None, domain=None, id=None)
    stub_record.api_key = do_api_key

    mock_delete = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete')

    resource = Resource(stub_record)
    resource.delete()

    mock_delete.assert_called_once_with(ANY, headers=do_auth_header)


@pytest.mark.parametrize('record_id', [77238234, 235223])
def test_calls_response_with_delete_response(mocker, record_id):
    mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete',
        return_value=record_id)
    stub_record = mocker.MagicMock(spec=Record)

    mock_response = mocker.patch(
        'lets_do_dns.do_domain.resource.Response')

    resource = Resource(stub_record())
    resource.delete()

    mock_response.assert_called_with(record_id)
