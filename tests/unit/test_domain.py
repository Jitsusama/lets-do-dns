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
