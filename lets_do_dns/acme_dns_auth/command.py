"""Wrap subprocess module."""
from subprocess import check_call


def run(command):
    """Run specified command through shell and verify result."""
    check_call(command, shell=True)
