"""Errors That May Be Encountered While Interfacing With This Package."""


class RequiredInputMissing(ValueError):
    """Triggered when a required environment variable is missing."""
    pass


class AuthenticationFailure(RuntimeError):
    """An error was encountered during ownership authentication."""
    pass


class RecordCreationFailure(AuthenticationFailure):
    """An error was encountered while attempting to create a record."""
    pass


class RecordLookupFailure(AuthenticationFailure):
    """An error was encountered while verifying DNS record existence."""
    pass
