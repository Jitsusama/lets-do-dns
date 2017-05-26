from subprocess import CalledProcessError
import pytest
from lets_do_dns.acme_dns_auth.command import run
from lets_do_dns.errors import PostCommandError


@pytest.mark.parametrize('command', [
    'do-important-stuff.sh', 'do-silly-stuff.sh --help'])
def test_run_properly_calls_check_call(mocker, command):
    stub_check_call = mocker.patch(
        'lets_do_dns.acme_dns_auth.command.check_call')

    run(command)

    stub_check_call.assert_called_once_with(command, shell=True)


def test_run_wraps_subprocess_exception_in_command_error(mocker):
    stub_called_process_error = CalledProcessError(
        returncode=1, cmd='stub-command')
    mocker.patch(
        'lets_do_dns.acme_dns_auth.command.check_call',
        side_effect=stub_called_process_error)

    mock_command_error = mocker.patch(
        'lets_do_dns.acme_dns_auth.command.PostCommandError',
        autospec=True, return_value=PostCommandError)

    with pytest.raises(PostCommandError):
        run('stub-command')

    mock_command_error.assert_called_once_with(stub_called_process_error)
