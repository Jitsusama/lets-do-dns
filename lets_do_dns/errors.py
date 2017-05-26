"""Errors that may be encountered while interfacing with this package."""


class BaseError(Exception):
    """Base error class for all lets_do_dns errors.

    These errors will have their string representation based on their
    docstring. As such, the first line of a subclassing exception's
    docstring should contain the message prefix that the exception will
    return when stringified.
    """

    def __str__(self):
        """Exception description followed by the first passed argument."""
        return '{}; {}'.format(self.message, self.args[0])

    @property
    def message(self):
        """Description of the exception."""
        docstring = self.__doc__
        first_line = docstring.splitlines().pop(0)
        period_suffix_removed = first_line.strip('.')

        return period_suffix_removed


class InputError(BaseError):
    """Missing one or more required environment variables."""


class HookError(BaseError):
    """Errors relating to a certbot hook stage."""

    hook_name = None

    @property
    def message(self):
        parent_message = super(HookError, self).message
        error_message = '{} during the {} hook stage'.format(
            parent_message, self.hook_name)

        return error_message


class AuthenticationError(HookError):
    """An error occurred during the authentication hook stage."""

    hook_name = 'authentication'


class CleanupError(HookError):
    """An error occurred during the authentication cleanup stage."""

    hook_name = 'cleanup'


class PostCommandError(CleanupError):
    """An error occurred while executing the post command."""

    def __str__(self):
        """Return parent text along with program output (if present)."""
        parent_str = super(PostCommandError, self).__str__()
        final_string = self._string_appended_with_command_output_text(
            parent_str)

        return final_string

    def _string_appended_with_command_output_text(self, text):
        command_output = self.args[0].output
        if not command_output:
            return text

        command_output = self._prepend_lines_with_spaces(
            command_output)
        final_string = '{} with the following text:\n\n{}'.format(
            text, command_output)

        return final_string

    @staticmethod
    def _prepend_lines_with_spaces(text):
        spaces = ' ' * 4
        prepended_lines = [
            '{}{}'.format(spaces, line) for line in text.splitlines()]

        return '\n'.join(prepended_lines)


class RecordCreationError(AuthenticationError):
    """An error occurred while creating the authentication record."""


class RecordDeletionError(CleanupError):
    """An error occurred while deleting the authentication record."""


class RecordLookupError(AuthenticationError):
    """An error occurred while verifying the authentication record."""
