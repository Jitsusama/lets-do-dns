import pytest

from lets_do_dns.errors import (
    BaseError, AuthenticationError, CleanupError, HookError,
    RecordCreationError, RecordDeletionError, RecordLookupError,
    RequiredInputMissingError)


@pytest.mark.parametrize(
    'child_exception', [RecordCreationError, RecordDeletionError,
                        RecordLookupError, RequiredInputMissingError])
def test_docstring_based_message_errors_have_docstring(child_exception):
    assert child_exception.__doc__


@pytest.mark.parametrize(
    'hook_exception', [AuthenticationError, CleanupError])
def test_hook_errors_contain_hook_name(hook_exception):
    assert hook_exception.hook_name


class TestInheritance(object):
    @pytest.mark.parametrize(
        'exception', [HookError, RequiredInputMissingError])
    def test_base_errors(self, exception):
        assert issubclass(exception, BaseError)

    @pytest.mark.parametrize(
        'child_exception', [AuthenticationError, CleanupError])
    def test_hook_errors(self, child_exception):
        assert issubclass(child_exception, HookError)

    @pytest.mark.parametrize(
        'child_exception', [RecordCreationError, RecordLookupError])
    def test_authentication_errors(
            self, child_exception):
        assert issubclass(child_exception, AuthenticationError)

    def test_cleanup_errors(self):
        assert issubclass(RecordDeletionError, CleanupError)


class TestBaseError(object):
    def test_message_returns_first_line_of_docstring(self):
        error = BaseError()
        error.__doc__ = 'first-line\nsecond-line'

        assert error.message == 'first-line'

    def test_message_trims_period_from_end_of_docstring(self, mocker):
        stub_exception = mocker.Mock(
            spec=Exception, __str__=lambda _: 'stub-exception')

        error = BaseError(stub_exception)
        error.__doc__ = 'message ending with a period.'

        assert error.message == 'message ending with a period'

    def test___str___includes_message(self, mocker):
        stub_exception = mocker.Mock(
            spec=Exception, __str__=lambda _: 'stub-exception')

        mock_message = mocker.patch(
            'lets_do_dns.errors.BaseError.message',
            new_callable=mocker.PropertyMock, return_value='stub-string')

        str(BaseError(stub_exception))

        mock_message.assert_called_once()

    def test___str___includes_passed_exception(self, mocker):
        stub_exception = mocker.Mock(
            spec=Exception, __str__=lambda _: 'stub-exception')

        error = BaseError(stub_exception)
        error.__doc__ = 'stub-docstring'
        message = str(error)

        assert 'stub-exception' in message


class TestHookError(object):
    def test_message_includes_parent_message_(self, mocker):
        stub_message = mocker.PropertyMock(return_value='stub-message')
        mocker.patch(
            'lets_do_dns.errors.BaseError.message',
            new=stub_message)

        error = HookError('stub-exception')

        assert 'stub-message' in error.message

    @pytest.mark.parametrize(
        'hook_under_test', ['authentication', 'cleanup'])
    def test_message_includes_stage_information(self, hook_under_test):
        error = HookError('stub-exception')
        error.hook_name = hook_under_test

        assert hook_under_test in error.message
