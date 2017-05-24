import pytest

from lets_do_dns.errors import (
    AuthenticationError, RecordCreationError, RecordDeletionError,
    RecordLookupError)


@pytest.mark.parametrize(
    'child_exception', [RecordCreationError, RecordDeletionError,
                        RecordLookupError])
def test_authentication_errors_inherit_from_base_error(
        child_exception):
    assert issubclass(child_exception, AuthenticationError)


@pytest.mark.parametrize(
    'child_exception', [RecordCreationError, RecordDeletionError,
                        RecordLookupError])
def test_authentication_errors_have_docstring(child_exception):
    assert child_exception.__doc__


class TestAuthenticationFailures(object):
    @pytest.mark.parametrize('docstring', ['first-string',
                                           'second-string'])
    def test_message_returns_first_line_of_docstring(self, docstring):
        failure = AuthenticationError()
        failure.__doc__ = docstring

        assert docstring in failure.message

    def test___str___includes_message(self, mocker):
        stub_exception = mocker.Mock(
            spec=Exception, __str__=lambda _: 'stub-message')

        mock_message = mocker.patch(
            'lets_do_dns.errors.AuthenticationError.message',
            new_callable=mocker.PropertyMock, return_value='stub-string')

        str(AuthenticationError(stub_exception))

        mock_message.assert_called_once()

    def test___str___includes_passed_exception(self, mocker):
        stub_exception = mocker.Mock(
            spec=Exception, __str__=lambda _: 'stub-message')

        message = str(AuthenticationError(stub_exception))

        assert 'stub-message' in message
