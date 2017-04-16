from certbot_dns_auth.printer import printer
from mock import call


def test_printer_writes_to_stdout(mocker):
    stub_stdout = mocker.patch('sys.stdout')

    printer(234567)

    stub_stdout.assert_has_calls([call.write('234567')])
