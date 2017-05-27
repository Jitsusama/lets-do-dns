"""Tests the lets_do_dns.do_domain.response.py module."""

from mock import call
import pytest
import requests
from requests.exceptions import HTTPError
from lets_do_dns.errors import RecordCreationError, RecordDeletionError

from lets_do_dns.do_domain.response import Response


def test_resource_id_returns_integer_on_post_request(mocker):
    stub_request = mocker.MagicMock(
        spec=requests.Request, method='POST')
    stub_post_response = mocker.MagicMock(
        spec=requests.Response, request=stub_request,
        json=lambda: {'domain_record': {'id': 23465545}})

    mock_response = Response(stub_post_response)

    assert mock_response.resource_id == 23465545


def test_resource_id_returns_nothing_on_delete_request(mocker):
    stub_request = mocker.MagicMock(
        spec=requests.Request, method='DELETE')
    stub_delete_response = mocker.MagicMock(
        spec=requests.Response, request=stub_request)

    mock_response = Response(stub_delete_response)

    assert mock_response.resource_id is None


def test_calls_raise_for_status(mocker):
    mock_post_response = mocker.MagicMock(spec=requests.Response)

    Response(mock_post_response)

    mock_post_response.assert_has_calls([call.raise_for_status()])


@pytest.mark.parametrize('method, exception', [
    ('POST', RecordCreationError), ('DELETE', RecordDeletionError)])
def test_properly_raises_correct_record_failure_on_related_method_error(
        mocker, method, exception):
    stub_error = HTTPError()
    stub_raise_for_status = mocker.MagicMock(side_effect=stub_error)
    stub_request = mocker.MagicMock(spec=requests.Request, method=method)
    stub_response = mocker.MagicMock(
        spec=requests.Response,
        raise_for_status=stub_raise_for_status, request=stub_request)

    class_to_mock = 'lets_do_dns.do_domain.response.{}'.format(
        exception.__name__)
    mock_record_failure = mocker.patch(
        class_to_mock, return_value=exception)

    with pytest.raises(exception):
        Response(stub_response)

    mock_record_failure.assert_called_once_with(stub_error)
