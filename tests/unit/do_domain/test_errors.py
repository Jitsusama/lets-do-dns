from lets_do_dns.do_domain.errors import exception_message
import pytest
import requests
import requests.exceptions


def test_exception_message_includes_request_uri(mocker):
    stub_request = mocker.Mock(
        spec=requests.Request, url='stub-uri', method='POST')
    stub_request_exception = mocker.Mock(
        spec=requests.exceptions.RequestException,
        request=stub_request, response=None)

    message = exception_message(stub_request_exception)

    assert 'stub-uri' in message


def test_exception_message_passed_response_includes_status_code(
        mocker):
    stub_request = mocker.MagicMock(
        spec=requests.Request, url='stub-uri', method='POST')
    stub_response = mocker.MagicMock(
        spec=requests.Response, status_code=500)
    stub_http_error_exception = mocker.MagicMock(
        spec=requests.exceptions.HTTPError,
        request=stub_request, response=stub_response)

    message = exception_message(stub_http_error_exception)

    assert '500' in message


@pytest.mark.parametrize('method', ['POST', 'DELETE'])
def test_exception_message_includes_method(mocker, method):
    stub_request = mocker.MagicMock(
        spec=requests.Request, url='stub-uri', method=method)
    stub_request_exception = mocker.Mock(
        spec=requests.exceptions.RequestException,
        request=stub_request, response=None)

    message = exception_message(stub_request_exception)

    assert method in message


def test_exception_message_includes_requests_error(mocker):
    stub_request = mocker.MagicMock(
        spec=requests.Request, url='stub-uri', method='POST')
    stub_str = mocker.MagicMock(return_value='message')
    stub_request_exception = mocker.Mock(
        spec=requests.exceptions.RequestException,
        request=stub_request, response=None, __str__=stub_str)

    message = exception_message(stub_request_exception)

    assert 'message' in message
