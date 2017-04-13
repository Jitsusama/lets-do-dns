from digitalocean.domain import Record
import pytest


@pytest.mark.parametrize('input_record_id', [345678, 456789])
def test_create_returns_record_id_from_created_dns_record(
        mocker, api_key, domain, hostname, auth_token, input_record_id):
    mocker.patch(
        'digitalocean.domain.http.create', return_value=input_record_id)

    record = Record(api_key, domain, hostname)
    output_record_id = record.create(auth_token)

    assert input_record_id == output_record_id


def test_create_properly_calls_http_create(
        mocker, api_key, domain, hostname, auth_token):
    stub_http_create = mocker.patch('digitalocean.domain.http.create')

    record = Record(api_key, domain, hostname)
    record.create(auth_token)

    stub_http_create.assert_called_once_with(
        api_key, domain, hostname, auth_token)
