"""Tests the lets_do_dns.do_domain.resource.py module."""

from mock import ANY, PropertyMock
import pytest
import requests.exceptions
from lets_do_dns.acme_dns_auth.record import Record
from lets_do_dns.errors import RecordCreationError

from lets_do_dns.do_domain.resource import Resource


def test_calls_post(mocker):
    stub_record = mocker.MagicMock(
        spec=Record, api_key=None, domain=None, id=None, hostname=None)

    mock_post = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post')

    resource = Resource(stub_record)
    resource.create()

    mock_post.assert_called_once()


def test_calls_post_with_correct_uri(mocker):
    stub_record = mocker.MagicMock(
        spec=Record, domain='grrbrr.ca',
        api_key=None, id=None, hostname=None)

    mock_post = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post')

    resource = Resource(stub_record)
    resource.create()

    expected_uri = (
        'https://api.digitalocean.com/v2/domains/grrbrr.ca/records')
    mock_post.assert_called_once_with(
        expected_uri, headers=ANY, json=ANY, timeout=ANY)


def test_calls_post_with_correct_authorization_header(mocker):
    stub_record = mocker.MagicMock(
        spec=Record, api_key='dummy-api-key',
        domain=None, id=None, hostname=None)

    mock_post = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post')

    resource = Resource(stub_record)
    resource.create()

    expected_auth_header = {'Authorization': 'Bearer dummy-api-key'}
    mock_post.assert_called_once_with(
        ANY, headers=expected_auth_header, json=ANY, timeout=ANY)


def test_calls_post_with_correct_json_body(mocker):
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
        ANY, headers=ANY, json=expected_json_request, timeout=ANY)


def test_calls_post_with_correct_timeouts(mocker):
    stub_record = mocker.MagicMock(
        spec=Record,
        hostname=None, api_key=None, domain=None, id=None)

    mock_post = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post')

    resource = Resource(stub_record, None)
    resource.create()

    mock_post.assert_called_once_with(
        ANY, headers=ANY, json=ANY, timeout=(10, 10))


def test_properly_calls_response(mocker):
    mocker.patch('lets_do_dns.do_domain.resource.requests.post',
                 return_value='stub-response')
    stub_record = mocker.MagicMock(
        spec=Record, hostname=None, api_key=None, domain=None, id=None)

    mock_response = mocker.patch(
        'lets_do_dns.do_domain.resource.Response')

    resource = Resource(stub_record)
    resource.create()

    mock_response.assert_called_once_with('stub-response')


def test_integer_property_accesses_resource_id(mocker):
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


@pytest.mark.parametrize(
    'requests_exception', [requests.exceptions.ConnectionError,
                           requests.exceptions.HTTPError,
                           requests.exceptions.Timeout])
def test_raises_authentication_failure_on_requests_exception(
        mocker, requests_exception):
    mocker.patch('lets_do_dns.do_domain.resource.requests.post',
                 side_effect=requests_exception)
    mocker.patch('lets_do_dns.do_domain.resource.Response')
    stub_record = mocker.MagicMock(
        spec=Record, hostname=None, api_key=None, domain=None, id=None)

    resource = Resource(stub_record)

    with pytest.raises(RecordCreationError):
        resource.create()


def test_passes_handled_exception_to_authentication_failure(
        mocker):
    stub_timeout = requests.exceptions.Timeout()
    stub_record = mocker.MagicMock(
        spec=Record, hostname=None, api_key=None, domain=None, id=None)
    mocker.patch('lets_do_dns.do_domain.resource.requests.post',
                 side_effect=stub_timeout)

    mock_record_creation_failure = mocker.patch(
        'lets_do_dns.do_domain.resource.RecordCreationError',
        return_value=RecordCreationError)

    resource = Resource(stub_record)

    with pytest.raises(RecordCreationError):
        resource.create()

    mock_record_creation_failure.assert_called_once_with(stub_timeout)
