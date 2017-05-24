"""Errors That May Be Encountered While Interfacing With This Package."""


class RequiredInputMissingError(ValueError):
    """Missing one or more required environment variables."""

    pass


class HookError(RuntimeError):
    """Parent class for errors relating to a certbot hook stage."""

    def __str__(self):
        """Formatted error message."""
        return '{}; {}'.format(self.message, self.args[0])

    @property
    def message(self):
        """Error message."""
        return self.__doc__


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
