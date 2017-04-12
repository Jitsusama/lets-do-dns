from acmednsauth.printer import Printer
from mock import call


def test_printer_writes_to_stdout(mocker):
    stdout = mocker.patch('sys.stdout')

    Printer(234567)

    stdout.assert_has_calls([call.write('234567')])
