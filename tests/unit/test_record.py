from do_record import Record
import pytest


@pytest.mark.parametrize('input_record_id', [345678, 456789])
def test_create_returns_record_id_from_created_dns_record(
        mocker, env, input_record_id):
    mocker.patch(
        'do_record.record.http.create', return_value=input_record_id)

    record = Record(env.key, env.domain, env.hostname)
    output_record_id = record.create(env.auth_token)

    assert input_record_id == output_record_id


def test_create_properly_calls_http_create(mocker, env):
    stub_http_create = mocker.patch('do_record.record.http.create')

    record = Record(env.key, env.domain, env.hostname)
    record.create(env.auth_token)

    stub_http_create.assert_called_once_with(record, env.auth_token)
