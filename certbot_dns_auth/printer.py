"""Handles the printing of messages."""


def printer(message):
    """Write messages to STDOUT."""
    not_none = message is not None
    not_empty = len(str(message)) > 0

    if not_none and not_empty:
        print message
