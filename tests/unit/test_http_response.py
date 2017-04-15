from do_record.http import response, RecordCreationFailure
import pytest


def test_returns_integer(fake_requests_response):
    fake_requests_response = fake_requests_response(201)
    fake_requests_response.id = 987123

    response_result = response(fake_requests_response)

    assert response_result == 987123


def test_raises_exception_on_bad_status_code(
        fake_requests_response):
    with pytest.raises(RecordCreationFailure):
        response(fake_requests_response(404))


def test_prints_response_status_code_with_raised_exception(
        fake_requests_response):
    with pytest.raises(RecordCreationFailure) as exception:
        response(fake_requests_response(500))

    assert str(exception).find('500') > 0


def test_prints_record_uri_with_raised_exception(
        env, fake_requests_response):
    with pytest.raises(RecordCreationFailure) as exception:
        response(fake_requests_response(600))

    expected_uri = 'https://api.digitalocean.com/v2/domains/%s/%s' % (
        env.domain, env.hostname)

    assert str(exception).find(expected_uri) > 0
