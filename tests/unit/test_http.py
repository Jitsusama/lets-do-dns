from do_record.http import create, response, RecordCreationFailure
from mock import ANY
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
        stub_requests = mocker.patch('do_record.http.requests.post')

        create(stub_record, AUTH_TOKEN)

        stub_requests.assert_called_once()

    def test_calls_correct_uri(self, mocker, stub_record):
        stub_requests = mocker.patch('do_record.http.requests.post')

        create(stub_record, AUTH_TOKEN)

        do_record_put_uri = (
            'https://api.digitalocean.com/v2/domains/grrbrr.ca/%s' % (
                HOSTNAME))

        stub_requests.assert_called_once_with(
            do_record_put_uri, headers=ANY)

    def test_passes_authorization_header(self, mocker, stub_record):
        stub_requests = mocker.patch('do_record.http.requests.post')

        create(stub_record, AUTH_TOKEN)

        stub_requests.assert_called_once_with(
            ANY, headers=AUTHORIZATION_HEADER)

    @pytest.mark.parametrize('input_record_id', [98765, 49586])
    def test_returns_integer_response(
            self, mocker, input_record_id, stub_record):
        mocker.patch('do_record.http.requests.post')
        mocker.patch(
            'do_record.http.response', return_value=input_record_id)

        create_response = create(stub_record, AUTH_TOKEN)

        assert create_response == input_record_id

    def test_calls_response_with_post_response(self, mocker, stub_record):
        mocker.patch('do_record.http.requests.post', return_value=1)
        stub_response = mocker.patch('do_record.http.response')

        create(stub_record, AUTH_TOKEN)

        stub_response.assert_called_with(1)


@pytest.fixture()
def fake_requests_response():
    class FakeRequestsResponse(object):
        def __init__(self, status_code):
            self.id = None
            self.status_code = status_code

        @property
        def ok(self): return self.status_code < 400

        def json(self):
            return {
                'domain_record': {
                    'id': self.id, 'type': 'TXT', 'name': HOSTNAME,
                    'data': AUTH_TOKEN, 'priority': None, 'port': None,
                    'weight': None}}

    return FakeRequestsResponse(201)


class TestResponse(object):
    def test_returns_integer(self, fake_requests_response):
        fake_requests_response.id = 987123

        response_result = response(fake_requests_response)

        assert response_result == 987123

    def test_raises_exception_on_bad_status_code(
            self, fake_requests_response):
        fake_requests_response.status_code = 404

        with pytest.raises(RecordCreationFailure):
            response(fake_requests_response)
