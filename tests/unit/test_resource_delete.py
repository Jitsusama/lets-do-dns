from mock import ANY
import pytest

from lets_do_dns.do_domain.resource import Resource
from lets_do_dns.acme_dns_auth.record import Record
from lets_do_dns.errors import AuthenticationFailure
from requests.exceptions import HTTPError


def test_calls_delete(mocker):
    stub_record = mocker.MagicMock(
        spec=Record, api_key=None, domain=None, id=None)

    mock_requests = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete')

    resource = Resource(stub_record)
    resource.delete()

    mock_requests.assert_called_once()


@pytest.mark.parametrize('record_id', [82227342, 2342552])
def test_calls_correct_uri(mocker, record_id):
    stub_record = mocker.MagicMock(
        spec=Record, domain='grrbrr.ca', id=record_id, api_key=None)

    mock_requests = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete')

    resource = Resource(stub_record)
    resource.delete()

    expected_uri = (
        'https://api.digitalocean.com/v2/domains/grrbrr.ca/records/%s'
        % record_id)
    mock_requests.assert_called_once_with(expected_uri, headers=ANY)


def test_passes_authorization_header(mocker):
    stub_record = mocker.MagicMock(
        spec=Record, api_key='dummy-api-key', domain=None, id=None)

    mock_delete = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete')

    resource = Resource(stub_record)
    resource.delete()

    expected_auth_header = {'Authorization': 'Bearer dummy-api-key'}
    mock_delete.assert_called_once_with(ANY, headers=expected_auth_header)


def test_calls_response_with_delete_response(mocker):
    mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete',
        return_value='mocked-response')
    stub_record = mocker.MagicMock(spec=Record)

    mock_response = mocker.patch(
        'lets_do_dns.do_domain.resource.Response')

    resource = Resource(stub_record())
    resource.delete()

    mock_response.assert_called_with('mocked-response')


def test_raises_authentication_failure_on_requests_exception(mocker):
    mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete',
        side_effect=HTTPError)
    stub_record = mocker.MagicMock(
        spec=Record, hostname=None, api_key=None, domain=None, id=None)

    resource = Resource(stub_record)

    with pytest.raises(AuthenticationFailure):
        resource.delete()
