"""Test Command Runner."""

from certbot_dns_auth.command import run
import pytest


@pytest.mark.parametrize('command', [
    'do-important-stuff.sh', 'do-silly-stuff.sh --help'])
def test_run_properly_calls_check_call(mocker, command):
    stub_check_call = mocker.patch('certbot_dns_auth.command.check_call')

    run(command)

    stub_check_call.assert_called_once_with("sh -c '" + command + "'")
