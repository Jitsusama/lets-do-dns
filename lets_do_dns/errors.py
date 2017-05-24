"""Errors That May Be Encountered While Interfacing With This Package."""


class RequiredInputMissingError(ValueError):
    """Missing one or more required environment variables."""
    pass


class AuthenticationError(RuntimeError):
    """An error was encountered during ownership authentication."""
    def __str__(self):
        return '{}; {}'.format(self.message, self.args[0])

    @property
    def message(self):
        return self.__doc__


class RecordCreationError(AuthenticationError):
    """An error was encountered while attempting to create a record."""
    pass


class RecordDeletionError(AuthenticationError):
    """An error occurred while deleting the authentication record."""
    pass


class RecordLookupError(AuthenticationError):
    """An error was encountered while verifying DNS record existence."""
    pass
