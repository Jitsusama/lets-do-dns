from do_record.http import delete
from mock import ANY
import pytest


def test_calls_delete(mocker, fake_record):
    stub_requests = mocker.patch('do_record.http.requests.delete')

    delete(fake_record(), 2322346)

    stub_requests.assert_called_once()


def test_does_not_return_value(mocker, fake_record):
    mocker.patch('do_record.http.requests.delete')

    assert delete(fake_record(), 2322346) is None


@pytest.mark.parametrize('record_id', [82227342, 2342552])
def test_calls_correct_uri(mocker, env, fake_record, record_id):
    stub_requests = mocker.patch('do_record.http.requests.delete')

    delete(fake_record(), record_id)

    record_delete_uri = (
        'https://api.digitalocean.com/v2/domains/%s/records/%s' % (
            env.domain, record_id))

    stub_requests.assert_called_once_with(record_delete_uri, headers=ANY)


@pytest.mark.parametrize('record_id', [4323422, 1231123])
def test_passes_authorization_header(mocker, env, fake_record, record_id):
    stub_requests = mocker.patch('do_record.http.requests.delete')

    delete(fake_record(), record_id)

    stub_requests.assert_called_once_with(ANY, headers=env.auth_header)


@pytest.mark.parametrize('record_id', [77238234, 235223])
def test_calls_response_with_post_response(
        mocker, fake_record, record_id):
    mocker.patch('do_record.http.requests.delete', return_value=record_id)
    stub_response = mocker.patch('do_record.http.response')

    delete(fake_record(), record_id)

    stub_response.assert_called_with(record_id)
