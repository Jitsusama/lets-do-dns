from certbot_dns_auth.printer import printer
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
