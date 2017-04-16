from certbot_dns_auth import Authenticate
import pytest


@pytest.mark.parametrize('record_id', [987623])
def test_digitalocean_authentication_record_creation(
        mocker, fake_requests_response, create_environment,
        record_id):
    mock_post_response = fake_requests_response(201)
    mock_post_response.id = record_id

    mocker.patch('do_record.http.requests.post',
                 return_value=mock_post_response)
    stub_printer = mocker.patch('certbot_dns_auth.authenticate.printer')

    authentication = Authenticate(environment=create_environment)
    authentication.perform()

    stub_printer.assert_called_once_with(record_id)


@pytest.mark.parametrize('record_id', [539283])
def test_digitalocean_authentication_record_deletion(
        mocker, fake_requests_response, delete_environment,
        record_id):
    mock_delete_response = fake_requests_response(204)

    mock_delete = mocker.patch(
        'do_record.http.requests.delete',
        return_value=mock_delete_response)

    authentication = Authenticate(
        environment=delete_environment(record_id))
    authentication.perform()

    mock_delete.assert_called_once_with(record_id)
