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
        suffixing_periods_removed = first_line.strip('.')

        return suffixing_periods_removed


class RequiredInputMissingError(BaseError):
    """Missing one or more required environment variables."""


class HookError(BaseError):
    """Errors relating to a certbot hook stage."""


class AuthenticationError(HookError):
    """An error occurred during the authentication hook stage."""


class CleanupError(HookError):
    """An error occurred during the authentication cleanup stage."""


class RecordCreationError(AuthenticationError):
    """An error occurred while creating the authentication record."""


class RecordDeletionError(CleanupError):
    """An error occurred while deleting the authentication record."""


class RecordLookupError(AuthenticationError):
    """An error occurred while verifying the authentication record."""
