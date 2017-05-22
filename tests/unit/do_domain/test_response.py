from mock import call
import pytest
import requests
from requests.exceptions import HTTPError

from lets_do_dns.errors import RecordCreationFailure
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


def test_passes_requests_exception_to_record_creation_failure(mocker):
    stub_error = HTTPError()
    stub_raise_for_status = mocker.MagicMock(
        side_effect=stub_error)
    stub_post_response = mocker.MagicMock(
        spec=requests.Response,
        raise_for_status=stub_raise_for_status)

    mock_record_creation_failure = mocker.patch(
        'lets_do_dns.do_domain.response.RecordCreationFailure',
        return_value=RecordCreationFailure)

    with pytest.raises(RecordCreationFailure):
        Response(stub_post_response)

    mock_record_creation_failure.assert_called_once_with(stub_error)
