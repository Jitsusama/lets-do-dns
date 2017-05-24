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


class TestAuthenticationFailures(object):
    @pytest.mark.parametrize('docstring', ['first-string',
                                           'second-string'])
    def test_message_returns_first_line_of_docstring(self, docstring):
        failure = AuthenticationFailure()
        failure.__doc__ = docstring

        assert docstring in failure.message

    def test___str___includes_message(self, mocker):
        stub_exception = mocker.Mock(
            spec=Exception, __str__=lambda _: 'stub-message')

        mock_message = mocker.patch(
            'lets_do_dns.errors.AuthenticationFailure.message',
            new_callable=mocker.PropertyMock, return_value='stub-string')

        str(AuthenticationFailure(stub_exception))

        mock_message.assert_called_once()

    def test___str___includes_passed_exception(self, mocker):
        stub_exception = mocker.Mock(
            spec=Exception, __str__=lambda _: 'stub-message')

        message = str(AuthenticationFailure(stub_exception))

        assert 'stub-message' in message
