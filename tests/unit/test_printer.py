from certbot_dns_auth.printer import printer, stderr
from mock import call
import pytest


def test_printer_writes_to_stdout(mocker):
    stub_stdout = mocker.patch('sys.stdout.write')

    printer(234567)

    stub_stdout.assert_has_calls([call('234567')])


@pytest.mark.parametrize('message', ['', None])
def test_printer_writes_nothing_with_empty_message(mocker, message):
    stub_stdout = mocker.patch('sys.stdout.write')

    printer(message)

    stub_stdout.assert_not_called()


def test_stderr_writes_to_stderr(mocker):
    stub_stderr = mocker.patch('sys.stderr.write')

    stderr('error message')

    stub_stderr.assert_has_calls([call('error message')])


@pytest.mark.parametrize('message', ['', None])
def test_stderr_writes_nothing_with_empty_message(mocker, message):
    stub_stderr = mocker.patch('sys.stderr.write')

    stderr(message)

    stub_stderr.assert_not_called()
