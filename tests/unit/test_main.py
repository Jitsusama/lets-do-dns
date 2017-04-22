from certbot_dns_auth.__main__ import main
from certbot_dns_auth.errors import RequiredInputMissing
from mock import ANY, call
import pytest


def test_passes_environment_to_authenticate(mocker):
    mocker.patch('certbot_dns_auth.__main__.sys.exit')
    mocker.patch('certbot_dns_auth.__main__.Arguments')
    mocker.patch('certbot_dns_auth.__main__.Environment')

    stub_environment = mocker.patch(
        'certbot_dns_auth.__main__.os.environ')
    stub_authenticate = mocker.patch(
        'certbot_dns_auth.__main__.Authenticate')

    main()

    stub_authenticate.assert_called_once_with(stub_environment, ANY)


@pytest.mark.parametrize('return_code', [0, 1])
def test_exits_with_authenticates_return_code(mocker, return_code):
    mocker.patch('certbot_dns_auth.__main__.Authenticate.__init__',
                 return_value=None)
    mocker.patch('certbot_dns_auth.__main__.Authenticate.perform',
                 return_value=return_code)
    mocker.patch('certbot_dns_auth.__main__.Arguments')
    mocker.patch('certbot_dns_auth.__main__.Environment')

    stub_exit = mocker.patch('certbot_dns_auth.__main__.sys.exit')

    main()

    stub_exit.assert_called_once_with(return_code)


def test_passes_cli_arguments_to_arguments(mocker):
    arguments = ['lets-do-dns', '--help']

    mocker.patch('certbot_dns_auth.__main__.os.environ')
    mocker.patch('certbot_dns_auth.__main__.Authenticate')
    mocker.patch('certbot_dns_auth.__main__.Environment')
    mocker.patch('certbot_dns_auth.__main__.sys', argv=arguments)

    stub_arguments = mocker.patch('certbot_dns_auth.__main__.Arguments')

    main()

    stub_arguments.assert_called_once_with(arguments)


def test_passes_arguments_to_authenticate(mocker):
    mocker.patch('certbot_dns_auth.__main__.os.environ')
    mocker.patch('certbot_dns_auth.__main__.sys')
    mocker.patch('certbot_dns_auth.__main__.Environment')
    mocker.patch(
        'certbot_dns_auth.__main__.Arguments', return_value=1)

    stub_authenticate = mocker.patch(
        'certbot_dns_auth.__main__.Authenticate')

    main()

    stub_authenticate.assert_called_once_with(ANY, 1)


def test_passes_os_environ_to_environment(mocker):
    mocker.patch('certbot_dns_auth.__main__.sys')
    mocker.patch('certbot_dns_auth.__main__.Authenticate')
    mocker.patch('certbot_dns_auth.__main__.Arguments')

    stub_environ = mocker.patch('certbot_dns_auth.__main__.os.environ')
    stub_environment = mocker.patch(
        'certbot_dns_auth.__main__.Environment')

    main()

    stub_environment.assert_called_once_with(stub_environ)


def test_exits_with_code_two_when_environment_throws_missing_exception(
        mocker):
    mocker.patch('certbot_dns_auth.__main__.os.environ')
    mocker.patch('certbot_dns_auth.__main__.sys.argv')
    mocker.patch('certbot_dns_auth.__main__.Authenticate')
    mocker.patch('certbot_dns_auth.__main__.Arguments')
    mocker.patch('certbot_dns_auth.__main__.printer')
    mocker.patch(
        'certbot_dns_auth.__main__.Environment',
        side_effect=RequiredInputMissing())

    stub_exit = mocker.patch('certbot_dns_auth.__main__.sys.exit')

    main()

    stub_exit.assert_has_calls([call(2)])


def test_passes_environment_exception_message_to_printer(mocker):
    mocker.patch('certbot_dns_auth.__main__.os.environ')
    mocker.patch('certbot_dns_auth.__main__.sys')
    mocker.patch('certbot_dns_auth.__main__.Authenticate')
    mocker.patch('certbot_dns_auth.__main__.Arguments')
    mocker.patch(
        'certbot_dns_auth.__main__.Environment',
        side_effect=RequiredInputMissing('Missing Required Input'))

    stub_printer = mocker.patch('certbot_dns_auth.__main__.printer')

    main()

    stub_printer.assert_called_once_with('Missing Required Input')
