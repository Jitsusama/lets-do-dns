import sys
from lets_do_dns.printer import stdout, stderr
from mock import call
import pytest


def test_printer_writes_to_stdout(mocker):
    stub_stdout = mocker.patch('lets_do_dns.printer.print')

    stdout(234567)

    stub_stdout.assert_has_calls([call(234567)])


@pytest.mark.parametrize('message', ['', None])
def test_printer_writes_nothing_with_empty_message(mocker, message):
    stub_stdout = mocker.patch('lets_do_dns.printer.print')

    stdout(message)

    stub_stdout.assert_not_called()


def test_stderr_writes_to_stderr(mocker):
    stub_stderr = mocker.patch('lets_do_dns.printer.print')

    stderr('error message')

    stub_stderr.assert_has_calls([call('error message', file=sys.stderr)])


@pytest.mark.parametrize('message', ['', None])
def test_stderr_writes_nothing_with_empty_message(mocker, message):
    stub_stderr = mocker.patch('lets_do_dns.printer.print')

    stderr(message)

    stub_stderr.assert_not_called()
