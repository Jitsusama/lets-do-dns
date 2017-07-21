"""Tests the lets_do_dns.acme_dns_auth.command.py module."""

from subprocess import CalledProcessError, STDOUT
import pytest
from lets_do_dns.errors import PostCommandError

from lets_do_dns.acme_dns_auth.command import run


@pytest.mark.parametrize('command', [
    'do-important-stuff.sh', 'do-silly-stuff.sh --help'])
def test_properly_calls_check_output(mocker, command):
    mock_check_output = mocker.patch(
        'lets_do_dns.acme_dns_auth.command.check_output')

    run(command, None)

    mock_check_output.assert_called_once_with(
        command, env=mocker.ANY, shell=True, stderr=STDOUT)


@pytest.mark.parametrize('hostname', ['stub-host1', 'stub-host2'])
def test_passes_certbot_hostname_in_env(mocker, hostname):
    mock_check_output = mocker.patch(
        'lets_do_dns.acme_dns_auth.command.check_output')

    run('stub-command', {'CERTBOT_HOSTNAME': hostname})

    mock_check_output.assert_called_once_with(
        mocker.ANY, env={'CERTBOT_HOSTNAME': hostname},
        shell=mocker.ANY, stderr=mocker.ANY)


def test_wraps_subprocess_exception_in_command_error(mocker):
    stub_called_process_error = CalledProcessError(
        returncode=1, cmd='stub-command')
    mocker.patch(
        'lets_do_dns.acme_dns_auth.command.check_output',
        side_effect=stub_called_process_error)

    mock_command_error = mocker.patch(
        'lets_do_dns.acme_dns_auth.command.PostCommandError',
        autospec=True, return_value=PostCommandError)

    with pytest.raises(PostCommandError):
        run('stub-command', None)

    mock_command_error.assert_called_once_with(stub_called_process_error)
