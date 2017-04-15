from do_record.http import create
from mock import ANY
import pytest


def test_calls_post(mocker, env, fake_record):
    stub_requests = mocker.patch('do_record.http.requests.post')

    create(fake_record(), env.auth_token)

    stub_requests.assert_called_once()


def test_calls_correct_uri(mocker, env, fake_record):
    stub_requests = mocker.patch('do_record.http.requests.post')

    create(fake_record(), env.auth_token)

    do_record_put_uri = (
        'https://api.digitalocean.com/v2/domains/%s/%s' % (
            env.domain, env.hostname))

    stub_requests.assert_called_once_with(
        do_record_put_uri, headers=ANY)


def test_passes_authorization_header(mocker, env, fake_record):
    stub_requests = mocker.patch('do_record.http.requests.post')

    create(fake_record(), env.auth_token)

    stub_requests.assert_called_once_with(
        ANY, headers=env.auth_header)


@pytest.mark.parametrize('input_record_id', [98765, 49586])
def test_returns_integer_response(
        mocker, env, input_record_id, fake_record):
    mocker.patch('do_record.http.requests.post')
    mocker.patch(
        'do_record.http.response', return_value=input_record_id)

    create_response = create(fake_record(), env.auth_token)

    assert create_response == input_record_id


def test_calls_response_with_post_response(mocker, env, fake_record):
    mocker.patch('do_record.http.requests.post', return_value=1)
    stub_response = mocker.patch('do_record.http.response')

    create(fake_record(), env.auth_token)

    stub_response.assert_called_with(1)
