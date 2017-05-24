import pytest

from lets_do_dns.errors import (
    AuthenticationError, CleanupError, HookError,
    RecordCreationError, RecordDeletionError, RecordLookupError)


@pytest.mark.parametrize(
    'child_exception', [AuthenticationError, CleanupError])
def test_hook_errors_inherit_from_hook_error(child_exception):
    assert issubclass(child_exception, HookError)


@pytest.mark.parametrize(
    'child_exception', [RecordCreationError, RecordLookupError])
def test_authentication_errors_inherit_from_authentication_error(
        child_exception):
    assert issubclass(child_exception, AuthenticationError)


def test_cleanup_errors_inherit_from_cleanup_error():
    assert issubclass(RecordDeletionError, CleanupError)


@pytest.mark.parametrize(
    'child_exception', [RecordCreationError, RecordDeletionError,
                        RecordLookupError])
def test_final_hook_related_errors_have_docstring(child_exception):
    assert child_exception.__doc__


class TestHookError(object):
    @pytest.mark.parametrize(
        'docstring', ['first-string', 'second-string'])
    def test_message_returns_first_line_of_docstring(self, docstring):
        failure = HookError()
        failure.__doc__ = '{}\nsecond-line'.format(docstring)

        assert docstring == failure.message

    def test___str___includes_message(self, mocker):
        stub_exception = mocker.Mock(
            spec=Exception, __str__=lambda _: 'stub-message')

        mock_message = mocker.patch(
            'lets_do_dns.errors.HookError.message',
            new_callable=mocker.PropertyMock, return_value='stub-string')

        str(HookError(stub_exception))

        mock_message.assert_called_once()

    def test___str___includes_passed_exception(self, mocker):
        stub_exception = mocker.Mock(
            spec=Exception, __str__=lambda _: 'stub-message')

        message = str(HookError(stub_exception))

        assert 'stub-message' in message

    def test___str___trims_period_from_end_of_docstring(self, mocker):
        stub_exception = mocker.Mock(
            spec=Exception, __str__=lambda _: 'stub-message')

        exception = HookError(stub_exception)
        message = str(exception)

        docstring = (
            'Parent class for errors relating to a certbot hook stage;')

        assert message.startswith(docstring)
