from do_record.http import Response, RecordCreationFailure
import pytest


@pytest.mark.parametrize('record_id', [23465545])
def test_resource_id_returns_integer_on_post_request(
        fake_requests_post_response, record_id):
    fake_requests_post_response = fake_requests_post_response(201)
    fake_requests_post_response.id = record_id

    response_result = Response(fake_requests_post_response)

    assert response_result.resource_id == record_id


@pytest.mark.parametrize('record_id', [1245542])
def test_resource_id_returns_nothing_on_delete_request(
        fake_requests_delete_response, record_id):
    fake_requests_delete_response = fake_requests_delete_response(
        204, record_id)

    response_result = Response(fake_requests_delete_response)

    assert response_result.resource_id is None


def test_raises_exception_on_bad_status_code(
        fake_requests_post_response):
    with pytest.raises(RecordCreationFailure):
        Response(fake_requests_post_response(404))


def test_prints_response_status_code_with_raised_exception(
        fake_requests_post_response):
    with pytest.raises(RecordCreationFailure) as exception:
        Response(fake_requests_post_response(500))

    assert str(exception).find('500') > 0


def test_prints_record_uri_with_raised_exception(
        env, fake_requests_post_response):
    with pytest.raises(RecordCreationFailure) as exception:
        Response(fake_requests_post_response(600))

    expected_uri = ('https://api.digitalocean.com/v2/domains/'
                    '%s/records' % env.domain)

    assert str(exception).find(expected_uri) > 0
