"""Handles the printing of messages."""


def printer(message):
    """Write messages to STDOUT."""
    if message is not None and len(str(message)) > 0:
        print message
