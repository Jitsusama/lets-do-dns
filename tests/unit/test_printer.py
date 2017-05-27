"""Tests the lets_do_dns.printer.py module."""

import sys
from mock import call
import pytest

from lets_do_dns.printer import stdout, stderr


def test_stdout_properly_calls_print(mocker):
    mock_print = mocker.patch('lets_do_dns.printer.print')

    stdout(234567)

    mock_print.assert_has_calls([call(234567)])


@pytest.mark.parametrize('message', ['', None])
def test_stdout_does_not_call_print_with_empty_message(mocker, message):
    mock_print = mocker.patch('lets_do_dns.printer.print')

    stdout(message)

    mock_print.assert_not_called()


def test_stderr_properly_calls_print(mocker):
    mock_print = mocker.patch('lets_do_dns.printer.print')

    stderr('error message')

    mock_print.assert_has_calls([call('error message', file=sys.stderr)])


@pytest.mark.parametrize('message', ['', None])
def test_stderr_does_not_call_print_with_empty_message(mocker, message):
    mock_print = mocker.patch('lets_do_dns.printer.print')

    stderr(message)

    mock_print.assert_not_called()
