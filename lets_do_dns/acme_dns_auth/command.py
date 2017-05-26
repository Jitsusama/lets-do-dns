"""Wrap subprocess module."""

from subprocess import check_call, CalledProcessError

from lets_do_dns.errors import PostCommandError


def run(command):
    """Run specified command through shell and verify result."""
    try:
        check_call(command, shell=True)
    except CalledProcessError as exception:
        raise PostCommandError(exception)
