from do_record import Record
import pytest

API_KEY = 'super-duper-secret'
AUTH_TOKEN = 'validate-with-that'
DOMAIN = 'grrbrr.ca'
HOSTNAME = 'another-test-ssl-host'


@pytest.mark.parametrize('input_record_id', [345678, 456789])
def test_create_returns_record_id_from_created_dns_record(
        mocker, input_record_id):
    mocker.patch(
        'do_record.record.http.create', return_value=input_record_id)

    record = Record(API_KEY, DOMAIN, HOSTNAME)
    output_record_id = record.create(AUTH_TOKEN)

    assert input_record_id == output_record_id


def test_create_properly_calls_http_create(mocker):
    stub_http_create = mocker.patch('do_record.record.http.create')

    record = Record(API_KEY, DOMAIN, HOSTNAME)
    record.create(AUTH_TOKEN)

    stub_http_create.assert_called_once_with(record, AUTH_TOKEN)
