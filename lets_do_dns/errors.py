"""Errors That May Be Encountered While Interfacing With This Package."""


class RequiredInputMissingError(ValueError):
    """Missing one or more required environment variables."""

    pass


class HookError(RuntimeError):
    """Parent class for errors relating to a certbot hook stage.

    The first line of a subclassing exception's docstring should contain
    the message prefix that this exception will return when stringified.
    """

    def __str__(self):
        """Concatenated error message."""
        return '{}; {}'.format(self.message, self.args[0])

    @property
    def message(self):
        """Error message."""
        exception_docstring = self.__doc__
        first_line_of_docstring = exception_docstring.splitlines().pop(0)
        final_message = first_line_of_docstring.strip('.')

        return final_message


class AuthenticationError(HookError):
    """An error occurred during the authentication hook stage."""

    pass


class CleanupError(HookError):
    """An error occurred during the authentication cleanup stage."""

    pass


class RecordCreationError(AuthenticationError):
    """An error occurred while creating the authentication record."""

    pass


class RecordDeletionError(CleanupError):
    """An error occurred while deleting the authentication record."""

    pass


class RecordLookupError(AuthenticationError):
    """An error occurred while verifying the authentication record."""

    pass
