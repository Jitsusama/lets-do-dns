"""Tests the lets_do_dns.do_domain.resource.py module."""

from mock import ANY, PropertyMock
import pytest
import requests.exceptions
from lets_do_dns.errors import RecordCreationError

from lets_do_dns.do_domain.resource import Resource


def test_calls_post(mocker):
    mock_post = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post')

    resource = Resource('stub-api-key', 'stub-host', 'stub-domain')
    resource.create()

    mock_post.assert_called_once()


def test_calls_post_with_correct_uri(mocker):
    mock_post = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post')

    resource = Resource('stub-api-key', 'stub-host', 'stub-domain')
    resource.create()

    expected_uri = (
        'https://api.digitalocean.com/v2/domains/stub-domain/records')
    mock_post.assert_called_once_with(
        expected_uri, headers=ANY, json=ANY, timeout=ANY)


def test_calls_post_with_correct_authorization_header(mocker):
    mock_post = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post')

    resource = Resource('stub-api-key', 'stub-host', 'stub-domain')
    resource.create()

    expected_auth_header = {'Authorization': 'Bearer stub-api-key'}
    mock_post.assert_called_once_with(
        ANY, headers=expected_auth_header, json=ANY, timeout=ANY)


def test_calls_post_with_correct_json_body(mocker):
    mock_post = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post')

    resource = Resource(
        'stub-api-key', 'stub-host', 'stub-domain', 'stub-auth-token')
    resource.create()

    expected_json_request = {
        'type': 'TXT',
        'name': 'stub-host',
        'data': 'stub-auth-token'}
    mock_post.assert_called_once_with(
        ANY, headers=ANY, json=expected_json_request, timeout=ANY)


def test_calls_post_with_correct_timeouts(mocker):
    mock_post = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post')

    resource = Resource('stub-api-key', 'stub-host', 'stub-domain')
    resource.create()

    mock_post.assert_called_once_with(
        ANY, headers=ANY, json=ANY, timeout=(10, 10))


def test_properly_calls_response(mocker):
    mocker.patch('lets_do_dns.do_domain.resource.requests.post',
                 return_value='stub-response')

    mock_response = mocker.patch(
        'lets_do_dns.do_domain.resource.Response')

    resource = Resource('stub-api-key', 'stub-host', 'stub-domain')
    resource.create()

    mock_response.assert_called_once_with('stub-response')


def test_integer_property_accesses_resource_id(mocker):
    mocker.patch('lets_do_dns.do_domain.resource.requests.post')
    mocker.patch('lets_do_dns.do_domain.resource.Response.__init__',
                 return_value=None)

    mock_resource_id = mocker.patch(
        'lets_do_dns.do_domain.resource.Response.resource_id',
        new_callable=PropertyMock)

    resource = Resource('stub-api-key', 'stub-host', 'stub-domain')
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

    resource = Resource('stub-api-key', 'stub-host', 'stub-domain')
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

    resource = Resource('stub-api-key', 'stub-host', 'stub-domain')

    with pytest.raises(RecordCreationError):
        resource.create()


def test_passes_handled_exception_to_authentication_failure(
        mocker):
    stub_timeout = requests.exceptions.Timeout()
    mocker.patch('lets_do_dns.do_domain.resource.requests.post',
                 side_effect=stub_timeout)

    mock_record_creation_failure = mocker.patch(
        'lets_do_dns.do_domain.resource.RecordCreationError',
        return_value=RecordCreationError)

    resource = Resource('stub-api-key', 'stub-host', 'stub-domain')

    with pytest.raises(RecordCreationError):
        resource.create()

    mock_record_creation_failure.assert_called_once_with(stub_timeout)
