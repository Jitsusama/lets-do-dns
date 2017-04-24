from certbot_dns_auth.__main__ import main
from certbot_dns_auth.errors import RequiredInputMissing
from mock import ANY, call
import pytest


class TestAuthenticateInteractions(object):
    def test_passed_environment(self, mocker):
        mocker.patch('certbot_dns_auth.__main__.sys.exit')
        mocker.patch('certbot_dns_auth.__main__.Arguments')
        mocker.patch('certbot_dns_auth.__main__.Environment')

        stub_environment = mocker.patch(
            'certbot_dns_auth.__main__.os.environ')
        stub_authenticate = mocker.patch(
            'certbot_dns_auth.__main__.Authenticate')

        main()

        stub_authenticate.assert_called_once_with(stub_environment, ANY)

    def test_passed_arguments(self, mocker):
        mocker.patch('certbot_dns_auth.__main__.os.environ')
        mocker.patch('certbot_dns_auth.__main__.sys')
        mocker.patch('certbot_dns_auth.__main__.Environment')
        mocker.patch(
            'certbot_dns_auth.__main__.Arguments', return_value=1)

        stub_authenticate = mocker.patch(
            'certbot_dns_auth.__main__.Authenticate')

        main()

        stub_authenticate.assert_called_once_with(ANY, 1)

    @pytest.mark.parametrize('return_code', [0, 1])
    def test_performs_return_code_passed_to_sys_exit(
            self, mocker, return_code):
        mocker.patch('certbot_dns_auth.__main__.Authenticate.__init__',
                     return_value=None)
        mocker.patch('certbot_dns_auth.__main__.Authenticate.perform',
                     return_value=return_code)
        mocker.patch('certbot_dns_auth.__main__.Arguments')
        mocker.patch('certbot_dns_auth.__main__.Environment')

        stub_exit = mocker.patch('certbot_dns_auth.__main__.sys.exit')

        main()

        stub_exit.assert_called_once_with(return_code)


class TestArgumentsInteractions(object):
    def test_passed_cli_arguments(self, mocker):
        arguments = ['lets-do-dns', '--help']

        mocker.patch('certbot_dns_auth.__main__.os.environ')
        mocker.patch('certbot_dns_auth.__main__.Authenticate')
        mocker.patch('certbot_dns_auth.__main__.Environment')
        mocker.patch('certbot_dns_auth.__main__.sys', argv=arguments)

        stub_arguments = mocker.patch(
            'certbot_dns_auth.__main__.Arguments')

        main()

        stub_arguments.assert_called_once_with(arguments)


class TestEnvironmentInteractions(object):
    def test_passed_os_environ(self, mocker):
        mocker.patch('certbot_dns_auth.__main__.sys')
        mocker.patch('certbot_dns_auth.__main__.Authenticate')
        mocker.patch('certbot_dns_auth.__main__.Arguments')

        stub_environ = mocker.patch('certbot_dns_auth.__main__.os.environ')
        stub_environment = mocker.patch(
            'certbot_dns_auth.__main__.Environment')

        main()

        stub_environment.assert_called_once_with(stub_environ)

    def test_raised_error_code_passed_to_sys_exit(self, mocker):
        mocker.patch('certbot_dns_auth.__main__.os.environ')
        mocker.patch('certbot_dns_auth.__main__.sys.argv')
        mocker.patch('certbot_dns_auth.__main__.Authenticate')
        mocker.patch('certbot_dns_auth.__main__.Arguments')
        mocker.patch('certbot_dns_auth.__main__.stderr')
        mocker.patch(
            'certbot_dns_auth.__main__.Environment',
            side_effect=RequiredInputMissing())

        stub_exit = mocker.patch('certbot_dns_auth.__main__.sys.exit')

        main()

        stub_exit.assert_has_calls([call(2)])

    def test_raised_error_message_passed_to_stderr(self, mocker):
        mocker.patch('certbot_dns_auth.__main__.os.environ')
        mocker.patch('certbot_dns_auth.__main__.sys')
        mocker.patch('certbot_dns_auth.__main__.Authenticate')
        mocker.patch('certbot_dns_auth.__main__.Arguments')
        mocker.patch(
            'certbot_dns_auth.__main__.Environment',
            side_effect=RequiredInputMissing('Missing Required Input'))

        stub_printer = mocker.patch('certbot_dns_auth.__main__.stderr')

        main()

        stub_printer.assert_called_once_with('Missing Required Input')
