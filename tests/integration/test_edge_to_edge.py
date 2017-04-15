from acmednsauth.authenticate import Authenticate
import pytest


@pytest.mark.parametrize('record_id', [987623])
def test_digitalocean_authentication_record_creation(
        mocker, fake_requests_response, create_environment,
        record_id):
    fake_post_response = fake_requests_response(201)
    fake_post_response.id = record_id
    fake_delete_response = fake_requests_response(200)

    mocker.patch('do_record.http.requests.post',
                 return_value=fake_post_response)
    mocker.patch('do_record.http.requests.delete',
                 return_value=fake_delete_response)
    stub_printer = mocker.patch('acmednsauth.authenticate.printer')

    Authenticate(environment=create_environment)

    stub_printer.assert_called_once_with(record_id)
