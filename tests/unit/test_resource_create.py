import pytest
from mock import ANY, PropertyMock

from lets_do_dns.do_domain.resource import Resource
from lets_do_dns.acme_dns_auth.record import Record

# ATTENTION: Look at conftest.py for py.test fixture definitions.


def test_calls_post(mocker, certbot_auth_token):
    stub_record = mocker.MagicMock(
        spec=Record, api_key=None, domain=None, id=None, hostname=None)

    mock_requests = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post')

    resource = Resource(stub_record)
    resource.value = certbot_auth_token
    resource.create()

    mock_requests.assert_called_once()


def test_calls_correct_uri(
        mocker, do_domain, certbot_auth_token):
    stub_record = mocker.MagicMock(
        spec=Record, domain='grrbrr.ca',
        api_key=None, id=None, hostname=None)

    mock_requests = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post')

    resource = Resource(stub_record)
    resource.value = certbot_auth_token
    resource.create()

    do_record_put_uri = (
        'https://api.digitalocean.com/v2/domains/%s/records' % do_domain)
    mock_requests.assert_called_once_with(
        do_record_put_uri, headers=ANY, json=ANY)


def test_passes_authorization_header(
        mocker, do_auth_header, do_api_key):
    stub_record = mocker.MagicMock(
        spec=Record, api_key=do_api_key,
        domain=None, id=None, hostname=None)

    mock_requests = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post')

    resource = Resource(stub_record)
    resource.create()

    mock_requests.assert_called_once_with(
        ANY, headers=do_auth_header, json=ANY)


def test_passes_json_body(
        mocker, do_hostname, certbot_auth_token):
    stub_record = mocker.MagicMock(
        spec=Record, hostname=do_hostname,
        api_key=None, domain=None, id=None)

    mock_post = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post')

    resource = Resource(stub_record)
    resource.value = certbot_auth_token
    resource.create()

    json_request = {
        'type': 'TXT',
        'name': do_hostname,
        'data': certbot_auth_token,
    }
    mock_post.assert_called_once_with(ANY, headers=ANY, json=json_request)


def test_integer_property_properly_calls_response(
        mocker, certbot_auth_token, fake_requests_post_response):
    stub_record = mocker.MagicMock(
        spec=Record, hostname=None, api_key=None, domain=None, id=None)

    mock_post_response = fake_requests_post_response(201)

    mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post',
        return_value=mock_post_response)
    mock_response = mocker.patch(
        'lets_do_dns.do_domain.resource.Response')

    resource = Resource(stub_record)
    resource.value = certbot_auth_token
    resource.create()

    mock_response.assert_called_once_with(mock_post_response)


def test_integer_property_accesses_response_resource_id(
        mocker, fake_requests_post_response):
    stub_record = mocker.MagicMock(
        spec=Record, hostname=None, api_key=None, domain=None, id=None)
    stub_post_response = fake_requests_post_response(201)
    mocker.patch(
        'lets_do_dns.do_domain.resource.requests.post',
        return_value=stub_post_response)

    mocker.patch(
        'lets_do_dns.do_domain.resource.Response.__init__',
        return_value=None)
    mock_resource_id = mocker.patch(
        'lets_do_dns.do_domain.resource.Response.resource_id',
        new_callable=PropertyMock)

    resource = Resource(stub_record)
    resource.create()
    resource.__int__()

    mock_resource_id.assert_called_once()


@pytest.mark.parametrize('input_record_id', [98765, 49586])
def test_stores_integer_identifier(mocker, input_record_id):
    stub_record = mocker.MagicMock(
        spec=Record, hostname=None, api_key=None, domain=None, id=None)
    mocker.patch('lets_do_dns.do_domain.resource.requests.post')
    mocker.patch(
        'lets_do_dns.do_domain.resource.Response.__init__',
        return_value=None)
    mocker.patch(
        'lets_do_dns.do_domain.resource.Response.resource_id',
        new_callable=PropertyMock,
        return_value=input_record_id)

    resource = Resource(stub_record)
    resource.create()
    output_record_id = resource.__int__()

    assert output_record_id == input_record_id
