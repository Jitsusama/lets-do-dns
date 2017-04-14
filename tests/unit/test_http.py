from do_record.http import create
from mock import call, ANY
import pytest

API_KEY = (
    'b7e303ba3771d024c0f1a62b9b8d1ad35d4c7db5a2a6ce69962618eb89a9276c')
AUTHORIZATION_HEADER = {'Authorization': 'Bearer %s' % API_KEY}
AUTH_TOKEN = 'validate-with-this'
DOMAIN = 'grrbrr.ca'
HOSTNAME = 'test-ssl-host'


class StubRecord(object):
    def __init__(self, api_key, domain, hostname):
        self.api_key = api_key
        self.domain = domain
        self.hostname = hostname


def test_create_calls_correct_uri(
        mocker, api_key, domain, hostname, auth_token):
    fake_requests = mocker.patch('do_record.http.requests')
    stub_record = StubRecord(api_key, domain, hostname)

    create(stub_record, auth_token)

    do_record_put_uri = (
        'https://api.digitalocean.com/v2/domains/grrbrr.ca/%s' % hostname)
    call_put_properly = [call.put(do_record_put_uri, headers=ANY)]

    fake_requests.assert_has_calls(call_put_properly)


def test_create_passes_authorization_header(mocker):
    fake_requests = mocker.patch('do_record.http.requests')
    stub_record = StubRecord(API_KEY, DOMAIN, HOSTNAME)

    create(stub_record, AUTH_TOKEN)

    call_put_properly = [call.put(ANY, headers=AUTHORIZATION_HEADER)]

    fake_requests.assert_has_calls(call_put_properly)


@pytest.mark.parametrize('input_record_id', [98765, 49586])
def test_create_returns_response_object(mocker, input_record_id):
    mocker.patch('do_record.http.requests')
    mocker.patch('do_record.http.Response', return_value=input_record_id)
    stub_record = StubRecord(API_KEY, DOMAIN, HOSTNAME)

    response = create(stub_record, AUTH_TOKEN)

    assert int(response) == input_record_id
