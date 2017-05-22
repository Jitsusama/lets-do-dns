import pytest

from lets_do_dns.errors import (
    AuthenticationFailure, RecordCreationFailure, RecordLookupFailure)


@pytest.mark.parametrize(
    'child_exception', [RecordCreationFailure, RecordLookupFailure])
def test_authentication_errors_inherit_from_base_error(
        child_exception):
    assert issubclass(child_exception, AuthenticationFailure)


def test_record_creation_failure_str_properly_calls_exception_message(
        mocker):
    stub_exception = mocker.Mock()

    mock_exception_message = mocker.patch(
        'lets_do_dns.errors.api_errors.exception_message',
        return_value='stub_string')

    exception = RecordCreationFailure(stub_exception)
    str(exception)

    mock_exception_message.assert_called_once_with(stub_exception)
