"""Tests the lets_do_dns.do_domain.resource.py module."""

from mock import ANY
import pytest
import requests.exceptions
from lets_do_dns.acme_dns_auth.record import Record
from lets_do_dns.errors import RecordDeletionError

from lets_do_dns.do_domain.resource import Resource


def test_calls_delete(mocker):
    stub_record = mocker.MagicMock(
        spec=Record, api_key=None, domain=None, id=None)

    mock_delete = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete')

    resource = Resource(stub_record)
    resource.delete()

    mock_delete.assert_called_once()


@pytest.mark.parametrize('record_id', [82227342, 2342552])
def test_calls_delete_with_correct_uri(mocker, record_id):
    stub_record = mocker.MagicMock(
        spec=Record, domain='grrbrr.ca', id=record_id, api_key=None)

    mock_delete = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete')

    resource = Resource(stub_record)
    resource.delete()

    expected_uri = (
        'https://api.digitalocean.com/v2/domains/grrbrr.ca/records/%s'
        % record_id)
    mock_delete.assert_called_once_with(
        expected_uri, headers=ANY, timeout=ANY)


def test_calls_delete_with_correct_authorization_header(mocker):
    stub_record = mocker.MagicMock(
        spec=Record, api_key='dummy-api-key', domain=None, id=None)

    mock_delete = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete')

    resource = Resource(stub_record)
    resource.delete()

    expected_auth_header = {'Authorization': 'Bearer dummy-api-key'}
    mock_delete.assert_called_once_with(
        ANY, headers=expected_auth_header, timeout=ANY)


def test_calls_delete_with_correct_timeouts(mocker):
    stub_record = mocker.MagicMock(
        spec=Record,
        api_key=None, hostname=None, domain=None, id=None)

    mock_post = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete')

    resource = Resource(stub_record, None)
    resource.delete()

    mock_post.assert_called_once_with(
        ANY, headers=ANY, timeout=(6.3, 4.7))


def test_calls_response_with_delete_response(mocker):
    mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete',
        return_value='stub-response')
    stub_record = mocker.MagicMock(spec=Record)

    mock_response = mocker.patch(
        'lets_do_dns.do_domain.resource.Response')

    resource = Resource(stub_record())
    resource.delete()

    mock_response.assert_called_with('stub-response')


@pytest.mark.parametrize(
    'requests_exception', [requests.exceptions.ConnectionError,
                           requests.exceptions.HTTPError,
                           requests.exceptions.Timeout])
def test_raises_authentication_failure_on_requests_exception(
        mocker, requests_exception):
    mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete',
        side_effect=requests_exception)
    stub_record = mocker.MagicMock(
        spec=Record, hostname=None, api_key=None, domain=None, id=None)

    resource = Resource(stub_record)

    with pytest.raises(RecordDeletionError):
        resource.delete()


def test_passes_handled_exception_to_authentication_failure(
        mocker):
    stub_timeout = requests.exceptions.Timeout()
    stub_record = mocker.MagicMock(
        spec=Record, hostname=None, api_key=None, domain=None, id=None)
    mocker.patch('lets_do_dns.do_domain.resource.requests.delete',
                 side_effect=stub_timeout)

    mock_record_creation_failure = mocker.patch(
        'lets_do_dns.do_domain.resource.RecordDeletionError',
        return_value=RecordDeletionError)

    resource = Resource(stub_record)

    with pytest.raises(RecordDeletionError):
        resource.delete()

    mock_record_creation_failure.assert_called_once_with(stub_timeout)
