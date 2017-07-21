"""Wrap subprocess module."""

from subprocess import check_output, CalledProcessError, STDOUT

from lets_do_dns.errors import PostCommandError


def run(command, env):
    """Run specified command through shell and verify result."""
    try:
        check_output(command, env=env, shell=True, stderr=STDOUT)
    except CalledProcessError as exception:
        raise PostCommandError(exception)
