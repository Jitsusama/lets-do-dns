"""Tests the lets_do_dns.__main__.py module."""

from mock import call
from lets_do_dns.errors import HookError, InputError

from lets_do_dns.__main__ import main


class TestAuthenticateInteractions(object):
    def test_passes_environment(self, mocker):
        stub_environment = mocker.MagicMock()

        mocker.patch('lets_do_dns.__main__.os.environ')
        mocker.patch('lets_do_dns.__main__.sys.exit')
        mocker.patch('lets_do_dns.__main__.Arguments')
        mocker.patch('lets_do_dns.__main__.Environment',
                     return_value=stub_environment)

        mock_authenticate = mocker.patch(
            'lets_do_dns.__main__.Authenticate')

        main()

        mock_authenticate.assert_called_once_with(stub_environment)

    def test_raised_error_message_passed_to_stderr(
            self, mocker):
        mocker.patch.object(
            HookError, '__str__', lambda _: 'stub-message')
        mocker.patch('lets_do_dns.__main__.sys.exit')
        mocker.patch('lets_do_dns.__main__.Arguments')
        mocker.patch('lets_do_dns.__main__.Authenticate.__init__',
                     return_value=None)
        mocker.patch('lets_do_dns.__main__.Authenticate.perform',
                     side_effect=HookError('stub-message'))
        mocker.patch('lets_do_dns.__main__.Environment')

        mock_printer = mocker.patch('lets_do_dns.__main__.stderr')

        main()

        mock_printer.assert_called_once_with('stub-message')

    def test_raised_error_message_causes_error_code_2_on_exit(
            self, mocker):
        mocker.patch('lets_do_dns.__main__.sys.exit')
        mocker.patch('lets_do_dns.__main__.Arguments')
        mocker.patch('lets_do_dns.__main__.Authenticate.__init__',
                     return_value=None)
        mocker.patch('lets_do_dns.__main__.Authenticate.perform',
                     side_effect=HookError('stub-message'))
        mocker.patch('lets_do_dns.__main__.Environment')
        mocker.patch('lets_do_dns.__main__.stderr')

        mock_exit = mocker.patch('lets_do_dns.__main__.sys.exit')

        main()

        mock_exit.assert_called_once_with(2)


class TestArgumentsInteractions(object):
    def test_passes_cli_arguments(self, mocker):
        arguments = ['lets-do-dns', '--help']

        mocker.patch('lets_do_dns.__main__.os.environ')
        mocker.patch('lets_do_dns.__main__.sys', argv=arguments)
        mocker.patch('lets_do_dns.__main__.Authenticate')
        mocker.patch('lets_do_dns.__main__.Environment')

        mock_arguments = mocker.patch('lets_do_dns.__main__.Arguments')

        main()

        mock_arguments.assert_called_once_with(arguments)


class TestEnvironmentInteractions(object):
    def test_passes_os_environ(self, mocker):
        mocker.patch('lets_do_dns.__main__.sys')
        mocker.patch('lets_do_dns.__main__.Authenticate')
        mocker.patch('lets_do_dns.__main__.Arguments')
        stub_environ = mocker.patch('lets_do_dns.__main__.os.environ')

        mock_environment = mocker.patch('lets_do_dns.__main__.Environment')

        main()

        mock_environment.assert_called_once_with(stub_environ)

    def test_raised_error_causes_proper_call_to_sys_exit(self, mocker):
        mocker.patch('lets_do_dns.__main__.os.environ')
        mocker.patch('lets_do_dns.__main__.sys.argv')
        mocker.patch('lets_do_dns.__main__.Authenticate')
        mocker.patch('lets_do_dns.__main__.Arguments')
        mocker.patch('lets_do_dns.__main__.Environment',
                     side_effect=InputError('stub-message'))
        mocker.patch('lets_do_dns.__main__.stderr')

        mock_exit = mocker.patch('lets_do_dns.__main__.sys.exit')

        main()

        mock_exit.assert_has_calls([call(2)])

    def test_raised_error_message_passed_to_stderr(self, mocker):
        mocker.patch('lets_do_dns.__main__.os.environ')
        mocker.patch('lets_do_dns.__main__.sys')
        mocker.patch('lets_do_dns.__main__.Authenticate')
        mocker.patch('lets_do_dns.__main__.Arguments')
        mocker.patch('lets_do_dns.__main__.Environment',
                     side_effect=InputError('stub-message'))
        mocker.patch('lets_do_dns.__main__.InputError.__str__',
                     return_value='stub-message')

        mock_printer = mocker.patch('lets_do_dns.__main__.stderr')

        main()

        mock_printer.assert_called_once_with('stub-message')
