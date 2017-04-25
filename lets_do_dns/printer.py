"""Handles the printing of messages."""

from __future__ import print_function
import sys


def stdout(message):
    """Write message to STDOUT."""
    if _is_valid_message(message):
        print(message)


def stderr(message):
    """Write message to STDERR."""
    if _is_valid_message(message):
        print(message, file=sys.stderr)


def _is_valid_message(message):
    not_none = message is not None
    not_empty = len(str(message)) > 0

    return not_none and not_empty
