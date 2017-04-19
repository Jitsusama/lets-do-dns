from certbot_dns_auth.__main__ import main
import pytest


def test_passes_environment_to_authenticate(mocker):
    mocker.patch('certbot_dns_auth.__main__.sys.exit')

    stub_environment = mocker.patch(
        'certbot_dns_auth.__main__.os.environ')
    stub_authenticate = mocker.patch(
        'certbot_dns_auth.__main__.Authenticate')

    main()

    stub_authenticate.assert_called_once_with(stub_environment)


@pytest.mark.parametrize('return_code', [0, 1])
def test_exits_with_authenticates_return_code(mocker, return_code):
    mocker.patch(
        'certbot_dns_auth.__main__.Authenticate.__init__',
        return_value=None)
    mocker.patch(
        'certbot_dns_auth.__main__.Authenticate.perform',
        return_value=return_code)

    stub_exit = mocker.patch('certbot_dns_auth.__main__.sys.exit')

    main()

    stub_exit.assert_called_once_with(return_code)
