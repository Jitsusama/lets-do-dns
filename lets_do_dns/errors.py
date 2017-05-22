"""Errors That May Be Encountered While Interfacing With This Package."""

import lets_do_dns.do_domain.errors as api_errors


class RequiredInputMissing(ValueError):
    """Triggered when a required environment variable is missing."""
    pass


class AuthenticationFailure(RuntimeError):
    """An error was encountered during ownership authentication."""
    pass


class RecordCreationFailure(AuthenticationFailure):
    """An error was encountered while attempting to create a record.

    This exception wraps around an exception passed by a lower-level
    API; so it needs to be called with the wrapped exception."""
    def __str__(self):
        return api_errors.exception_message(self.args[0])


class RecordLookupFailure(AuthenticationFailure):
    """An error was encountered while verifying DNS record existence."""
    pass
