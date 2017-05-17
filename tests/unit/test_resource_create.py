from mock import ANY, PropertyMock
import pytest

from lets_do_dns.do_domain.resource import Resource
from lets_do_dns.acme_dns_auth.record import Record
from lets_do_dns.errors import AuthenticationFailure
from requests.exceptions import HTTPError


def test_calls_post(mocker):
    stub_record = mocker.MagicMock(
        spec=Record, api_key=None, domain=None, id=None, hostname=None)

    mock_requests = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post')

    resource = Resource(stub_record)
    resource.create()

    mock_requests.assert_called_once()


def test_calls_correct_uri(mocker):
    stub_record = mocker.MagicMock(
        spec=Record, domain='grrbrr.ca',
        api_key=None, id=None, hostname=None)

    mock_requests = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post')

    resource = Resource(stub_record)
    resource.create()

    expected_uri = (
        'https://api.digitalocean.com/v2/domains/grrbrr.ca/records')
    mock_requests.assert_called_once_with(
        expected_uri, headers=ANY, json=ANY)


def test_passes_authorization_header(mocker):
    stub_record = mocker.MagicMock(
        spec=Record, api_key='dummy-api-key',
        domain=None, id=None, hostname=None)

    mock_requests = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post')

    resource = Resource(stub_record)
    resource.create()

    expected_auth_header = {'Authorization': 'Bearer dummy-api-key'}
    mock_requests.assert_called_once_with(
        ANY, headers=expected_auth_header, json=ANY)


def test_passes_json_body(mocker):
    stub_record = mocker.MagicMock(
        spec=Record, hostname='dummy-hostname',
        api_key=None, domain=None, id=None)

    mock_post = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post')

    resource = Resource(stub_record, 'dummy-auth-token')
    resource.create()

    expected_json_request = {
        'type': 'TXT',
        'name': 'dummy-hostname',
        'data': 'dummy-auth-token'}
    mock_post.assert_called_once_with(
        ANY, headers=ANY, json=expected_json_request)


def test_integer_property_properly_calls_response(mocker):
    mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post',
        return_value='mocked-response')
    stub_record = mocker.MagicMock(
        spec=Record, hostname=None, api_key=None, domain=None, id=None)

    mock_response = mocker.patch(
        'lets_do_dns.do_domain.resource.Response')

    resource = Resource(stub_record)
    resource.create()

    mock_response.assert_called_once_with('mocked-response')


def test_integer_property_accesses_response_resource_id(mocker):
    mocker.patch('lets_do_dns.do_domain.resource.requests.post')
    mocker.patch('lets_do_dns.do_domain.resource.Response.__init__',
                 return_value=None)
    stub_record = mocker.MagicMock(
        spec=Record, hostname=None, api_key=None, domain=None, id=None)

    mock_resource_id = mocker.patch(
        'lets_do_dns.do_domain.resource.Response.resource_id',
        new_callable=PropertyMock)

    resource = Resource(stub_record)
    resource.create()
    resource.__int__()

    mock_resource_id.assert_called_once()


@pytest.mark.parametrize('input_record_id', [98765, 49586])
def test_stores_integer_identifier(mocker, input_record_id):
    mocker.patch('lets_do_dns.do_domain.resource.requests.post')
    mocker.patch('lets_do_dns.do_domain.resource.Response.__init__',
                 return_value=None)
    mocker.patch('lets_do_dns.do_domain.resource.Response.resource_id',
                 new_callable=PropertyMock,
                 return_value=input_record_id)
    stub_record = mocker.MagicMock(
        spec=Record, hostname=None, api_key=None, domain=None, id=None)

    resource = Resource(stub_record)
    resource.create()
    output_record_id = resource.__int__()

    assert output_record_id == input_record_id


def test_raises_authentication_failure_on_requests_exception(mocker):
    mocker.patch('lets_do_dns.do_domain.resource.requests.post',
                 side_effect=HTTPError)
    mocker.patch('lets_do_dns.do_domain.resource.Response')
    stub_record = mocker.MagicMock(
        spec=Record, hostname=None, api_key=None, domain=None, id=None)

    resource = Resource(stub_record)

    with pytest.raises(AuthenticationFailure):
        resource.create()
