from do_record.resource import Resource
from mock import ANY, PropertyMock
import pytest


def test_calls_post(mocker, env, fake_record):
    stub_requests = mocker.patch('do_record.resource.requests.post')

    resource = Resource(fake_record)
    resource.value = env.auth_token
    resource.create()

    stub_requests.assert_called_once()


def test_calls_correct_uri(mocker, env, fake_record):
    stub_requests = mocker.patch('do_record.resource.requests.post')

    resource = Resource(fake_record)
    resource.value = env.auth_token
    resource.create()

    do_record_put_uri = (
        'https://api.digitalocean.com/v2/domains/%s/records' % env.domain)

    stub_requests.assert_called_once_with(
        do_record_put_uri, headers=ANY, json=ANY)


def test_passes_authorization_header(mocker, env, fake_record):
    stub_requests = mocker.patch('do_record.resource.requests.post')

    resource = Resource(fake_record)
    resource.value = env.auth_token
    resource.create()

    stub_requests.assert_called_once_with(
        ANY, headers=env.auth_header, json=ANY)


def test_passes_json_body(mocker, env, fake_record):
    stub_post = mocker.patch('do_record.resource.requests.post')
    json_request = {
        'type': 'TXT',
        'name': env.hostname,
        'data': env.auth_token,
    }

    resource = Resource(fake_record)
    resource.value = env.auth_token
    resource.create()

    stub_post.assert_called_once_with(ANY, headers=ANY, json=json_request)


def test_integer_property_properly_calls_response(
        mocker, env, fake_record, fake_requests_post_response):
    mock_post_response = fake_requests_post_response(201)

    mocker.patch(
        'do_record.resource.requests.post',
        return_value=mock_post_response)
    stub_response = mocker.patch('do_record.resource.Response')

    resource = Resource(fake_record)
    resource.value = env.auth_token
    resource.create()

    stub_response.assert_called_once_with(mock_post_response)


def test_integer_property_accesses_response_resource_id(
        mocker, fake_record, fake_requests_post_response):
    mock_post_response = fake_requests_post_response(201)

    mocker.patch(
        'do_record.resource.requests.post', return_value=mock_post_response)
    mocker.patch(
        'do_record.resource.Response.__init__', return_value=None)
    stub_resource_id = mocker.patch(
        'do_record.resource.Response.resource_id',
        new_callable=PropertyMock)

    resource = Resource(fake_record)
    resource.create()
    resource.__int__()

    stub_resource_id.assert_called_once()


@pytest.mark.parametrize('input_record_id', [98765, 49586])
def test_stores_integer_identifier(
        mocker, env, input_record_id, fake_record):
    mocker.patch('do_record.resource.requests.post')
    mocker.patch(
        'do_record.resource.Response.__init__',
        return_value=None)
    mocker.patch(
        'do_record.resource.Response.resource_id',
        new_callable=PropertyMock,
        return_value=input_record_id)

    resource = Resource(fake_record)
    resource.value = env.auth_token
    resource.create()
    output_record_id = resource.__int__()

    assert output_record_id == input_record_id
