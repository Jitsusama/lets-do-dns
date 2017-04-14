from do_record.http import create
from mock import call, ANY
import pytest

API_KEY = 'shhhhhhhhh'
AUTHORIZATION_HEADER = {'Authorization': 'Bearer %s' % API_KEY}
AUTH_TOKEN = 'validate-with-another'
DOMAIN = 'grrbrr.ca'
HOSTNAME = 'test-ssl-hostie'


@pytest.fixture()
def stub_record():
    class StubRecord(object):
        def __init__(self, api_key, domain, hostname):
            self.api_key = api_key
            self.domain = domain
            self.hostname = hostname

    return StubRecord(API_KEY, DOMAIN, HOSTNAME)


class TestCreate(object):
    def test_calls_post(self, mocker, stub_record):
        fake_requests = mocker.patch('do_record.http.requests.post')

        create(stub_record, AUTH_TOKEN)

        fake_requests.assert_called_once()

    def test_calls_correct_uri(self, mocker, stub_record):
        fake_requests = mocker.patch('do_record.http.requests')

        create(stub_record, AUTH_TOKEN)

        do_record_put_uri = (
            'https://api.digitalocean.com/v2/domains/grrbrr.ca/%s' % (
                HOSTNAME))
        call_put_properly = [call.post(do_record_put_uri, headers=ANY)]

        fake_requests.assert_has_calls(call_put_properly)

    def test_passes_authorization_header(self, mocker, stub_record):
        fake_requests = mocker.patch('do_record.http.requests')

        create(stub_record, AUTH_TOKEN)

        call_put_properly = [call.post(ANY, headers=AUTHORIZATION_HEADER)]

        fake_requests.assert_has_calls(call_put_properly)

    @pytest.mark.parametrize('input_record_id', [98765, 49586])
    def test_returns_integer_response(
            self, mocker, input_record_id, stub_record):
        mocker.patch('do_record.http.requests')
        mocker.patch(
            'do_record.http.Response', return_value=input_record_id)

        response = create(stub_record, AUTH_TOKEN)

        assert int(response) == input_record_id
