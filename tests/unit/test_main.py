from mock import call
import pytest

from lets_do_dns.__main__ import main
from lets_do_dns.errors import HookError, RequiredInputMissingError


class TestAuthenticateInteractions(object):
    def test_passed_environment(self, mocker):
        stub_environment = mocker.MagicMock()

        mocker.patch('lets_do_dns.__main__.os.environ')
        mocker.patch('lets_do_dns.__main__.sys.exit')
        mocker.patch('lets_do_dns.__main__.Arguments')
        mocker.patch(
            'lets_do_dns.__main__.Environment',
            return_value=stub_environment)

        mock_authenticate = mocker.patch(
            'lets_do_dns.__main__.Authenticate')

        main()

        mock_authenticate.assert_called_once_with(stub_environment)

    @pytest.mark.parametrize('return_code', [0, 1])
    def test_performs_return_code_passed_to_sys_exit(
            self, mocker, return_code):
        mocker.patch('lets_do_dns.__main__.Authenticate.__init__',
                     return_value=None)
        mocker.patch('lets_do_dns.__main__.Authenticate.perform',
                     return_value=return_code)
        mocker.patch('lets_do_dns.__main__.Arguments')
        mocker.patch('lets_do_dns.__main__.Environment')

        mock_exit = mocker.patch('lets_do_dns.__main__.sys.exit')

        main()

        mock_exit.assert_called_once_with(return_code)

    def test_raised_error_message_passed_to_stderr(
            self, mocker):
        mocker.patch.object(
            HookError, '__str__', lambda _: 'Error Message')
        mocker.patch('lets_do_dns.__main__.Arguments')
        mocker.patch('lets_do_dns.__main__.Environment')
        mocker.patch('lets_do_dns.__main__.sys.exit')
        mocker.patch('lets_do_dns.__main__.Authenticate.__init__',
                     return_value=None)
        mocker.patch('lets_do_dns.__main__.Authenticate.perform',
                     side_effect=HookError('Error Message'))

        mock_printer = mocker.patch('lets_do_dns.__main__.stderr')

        main()

        mock_printer.assert_called_once_with('Error Message')

    def test_raised_error_message_causes_error_code_2_on_exit(
            self, mocker):
        mocker.patch('lets_do_dns.__main__.Arguments')
        mocker.patch('lets_do_dns.__main__.Environment')
        mocker.patch('lets_do_dns.__main__.sys.exit')
        mocker.patch('lets_do_dns.__main__.Authenticate.__init__',
                     return_value=None)
        mocker.patch('lets_do_dns.__main__.Authenticate.perform',
                     side_effect=HookError('Error Message'))
        mocker.patch('lets_do_dns.__main__.stderr')

        mock_exit = mocker.patch('lets_do_dns.__main__.sys.exit')

        main()

        mock_exit.assert_called_once_with(2)


class TestArgumentsInteractions(object):
    def test_passed_cli_arguments(self, mocker):
        arguments = ['lets-do-dns', '--help']

        mocker.patch('lets_do_dns.__main__.os.environ')
        mocker.patch('lets_do_dns.__main__.Authenticate')
        mocker.patch('lets_do_dns.__main__.Environment')
        mocker.patch('lets_do_dns.__main__.sys', argv=arguments)

        mock_arguments = mocker.patch(
            'lets_do_dns.__main__.Arguments')

        main()

        mock_arguments.assert_called_once_with(arguments)


class TestEnvironmentInteractions(object):
    def test_passed_os_environ(self, mocker):
        mocker.patch('lets_do_dns.__main__.sys')
        mocker.patch('lets_do_dns.__main__.Authenticate')
        mocker.patch('lets_do_dns.__main__.Arguments')
        stub_environ = mocker.patch('lets_do_dns.__main__.os.environ')

        mock_environment = mocker.patch(
            'lets_do_dns.__main__.Environment')

        main()

        mock_environment.assert_called_once_with(stub_environ)

    def test_raised_error_code_passed_to_sys_exit(self, mocker):
        mocker.patch('lets_do_dns.__main__.os.environ')
        mocker.patch('lets_do_dns.__main__.sys.argv')
        mocker.patch('lets_do_dns.__main__.Authenticate')
        mocker.patch('lets_do_dns.__main__.Arguments')
        mocker.patch('lets_do_dns.__main__.stderr')
        mocker.patch(
            'lets_do_dns.__main__.Environment',
            side_effect=RequiredInputMissingError('stub-message'))

        mock_exit = mocker.patch('lets_do_dns.__main__.sys.exit')

        main()

        mock_exit.assert_has_calls([call(2)])

    def test_raised_error_message_passed_to_stderr(self, mocker):
        mocker.patch('lets_do_dns.__main__.os.environ')
        mocker.patch('lets_do_dns.__main__.sys')
        mocker.patch('lets_do_dns.__main__.Authenticate')
        mocker.patch('lets_do_dns.__main__.Arguments')
        mocker.patch(
            'lets_do_dns.__main__.RequiredInputMissingError.__str__',
            return_value='stub-message')
        mocker.patch(
            'lets_do_dns.__main__.Environment',
            side_effect=RequiredInputMissingError('stub-message'))

        mock_printer = mocker.patch('lets_do_dns.__main__.stderr')

        main()

        mock_printer.assert_called_once_with('stub-message')
