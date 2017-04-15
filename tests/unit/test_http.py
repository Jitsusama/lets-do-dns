from do_record.http import create, response, RecordCreationFailure
from mock import ANY
import pytest


class TestCreate(object):
    def test_calls_post(self, mocker, env, fake_record):
        stub_requests = mocker.patch('do_record.http.requests.post')

        create(fake_record(), env.auth_token)

        stub_requests.assert_called_once()

    def test_calls_correct_uri(self, mocker, env, fake_record):
        stub_requests = mocker.patch('do_record.http.requests.post')

        create(fake_record(), env.auth_token)

        do_record_put_uri = (
            'https://api.digitalocean.com/v2/domains/%s/%s' % (
                env.domain, env.hostname))

        stub_requests.assert_called_once_with(
            do_record_put_uri, headers=ANY)

    def test_passes_authorization_header(self, mocker, env, fake_record):
        stub_requests = mocker.patch('do_record.http.requests.post')

        create(fake_record(), env.auth_token)

        stub_requests.assert_called_once_with(
            ANY, headers=env.auth_header)

    @pytest.mark.parametrize('input_record_id', [98765, 49586])
    def test_returns_integer_response(
            self, mocker, env, input_record_id, fake_record):
        mocker.patch('do_record.http.requests.post')
        mocker.patch(
            'do_record.http.response', return_value=input_record_id)

        create_response = create(fake_record(), env.auth_token)

        assert create_response == input_record_id

    def test_calls_response_with_post_response(
            self, mocker, env, fake_record):
        mocker.patch('do_record.http.requests.post', return_value=1)
        stub_response = mocker.patch('do_record.http.response')

        create(fake_record(), env.auth_token)

        stub_response.assert_called_with(1)


class TestResponse(object):
    def test_returns_integer(self, fake_requests_response):
        fake_requests_response = fake_requests_response(201)
        fake_requests_response.id = 987123

        response_result = response(fake_requests_response)

        assert response_result == 987123

    def test_raises_exception_on_bad_status_code(
            self, fake_requests_response):
        with pytest.raises(RecordCreationFailure):
            response(fake_requests_response(404))

    def test_prints_response_status_code_with_raised_exception(
            self, fake_requests_response):
        with pytest.raises(RecordCreationFailure) as exception:
            response(fake_requests_response(500))

        assert str(exception).find('500') > 0

    def test_prints_record_uri_with_raised_exception(
            self, env, fake_requests_response):
        with pytest.raises(RecordCreationFailure) as exception:
            response(fake_requests_response(600))

        expected_uri = 'https://api.digitalocean.com/v2/domains/%s/%s' % (
            env.domain, env.hostname)

        assert str(exception).find(expected_uri) > 0
