from do_record.record import Record
from mock import call
import pytest


@pytest.mark.parametrize('input_record_id', [491834, 882342])
def test_create_stores_record_id_internally(mocker, env, input_record_id):
    mocker.patch('do_record.resource.Resource.create')
    mocker.patch(
        'do_record.resource.Resource.__int__',
        return_value=input_record_id)

    record = Record(env.key, env.domain, env.hostname)
    record.create(env.auth_token)

    assert record.number == input_record_id


def test_create_properly_calls_http_create(mocker, env):
    stub_http_create = mocker.patch('do_record.record.Resource')

    record = Record(env.key, env.domain, env.hostname)
    record.create(env.auth_token)

    stub_http_create.assert_has_calls([
        call(record, env.auth_token),
        call().create()])


@pytest.mark.parametrize('record_id', [491834])
def test_delete_properly_calls_http_delete(mocker, env, record_id):
    stub_http_delete = mocker.patch('do_record.record.Resource')

    record = Record(env.key, env.domain, env.hostname)
    record.number = record_id
    record.delete()

    stub_http_delete.assert_has_calls([
        call(record),
        call().delete()])


def test_printer_calls_printer(mocker, env):
    stub_printer = mocker.patch('do_record.record.printer')
    record_id = 918342

    record = Record(env.key, env.domain, env.hostname)
    record.number = record_id
    record.printer()

    stub_printer.assert_called_once_with(record_id)
