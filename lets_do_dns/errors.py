"""Errors That May Be Encountered While Interfacing With This Package."""


class RequiredInputMissing(ValueError):
    """Triggered when a required environment variable is missing."""

    pass


class RecordCreationFailure(RuntimeError):
    """An error was encountered while attempting to create a record."""

    pass
