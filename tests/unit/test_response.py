import pytest
import requests

from lets_do_dns.errors import RecordCreationFailure
from lets_do_dns.do_domain.response import Response


@pytest.mark.parametrize('record_id', [23465545])
def test_resource_id_returns_integer_on_post_request(mocker, record_id):
    stub_request = mocker.MagicMock(
        spec=requests.Request, method='POST')
    stub_post_response = mocker.MagicMock(
        spec=requests.Response, request=stub_request,
        json=lambda: {'domain_record': {'id': record_id}})

    mock_response = Response(stub_post_response)

    assert mock_response.resource_id == record_id


@pytest.mark.parametrize('record_id', [1245542])
def test_resource_id_returns_nothing_on_delete_request(mocker, record_id):
    stub_request = mocker.MagicMock(
        spec=requests.Request, method='DELETE')
    stub_delete_response = mocker.MagicMock(
        spec=requests.Response, request=stub_request,
        json=lambda: {'domain_record': {'id': record_id}})

    mock_response = Response(stub_delete_response)

    assert mock_response.resource_id is None


def test_raises_exception_on_bad_status_code(mocker):
    stub_request = mocker.MagicMock(
        spec=requests.Request, method='POST')
    stub_post_response = mocker.MagicMock(
        spec=requests.Response, request=stub_request,
        status_code=404, ok=False, url=None)

    with pytest.raises(RecordCreationFailure):
        Response(stub_post_response)


def test_prints_response_status_code_with_raised_exception(mocker):
    stub_request = mocker.MagicMock(
        spec=requests.Request, method='POST')
    stub_requests_response = mocker.MagicMock(
        spec=requests.Response, request=stub_request,
        status_code=500, ok=False, url=None)

    with pytest.raises(RecordCreationFailure) as exception:
        Response(stub_requests_response)

    assert str(exception).find('500') > 0


def test_prints_record_uri_with_raised_exception(mocker):
    expected_uri = (
        'https://api.digitalocean.com/v2/domains/grrbrr.ca/records')

    stub_request = mocker.MagicMock(
        spec=requests.Request, method='POST')
    stub_requests_response = mocker.MagicMock(
        spec=requests.Response, request=stub_request,
        status_code=600, ok=False, url=expected_uri)

    with pytest.raises(RecordCreationFailure) as exception:
        Response(stub_requests_response)

    assert str(exception).find(expected_uri) > 0
