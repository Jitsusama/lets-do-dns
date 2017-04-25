"""Test Command Runner."""

import pytest

from certbot_dns_auth.dns01_auth.command import run


@pytest.mark.parametrize('command', [
    'do-important-stuff.sh', 'do-silly-stuff.sh --help'])
def test_run_properly_calls_check_call(mocker, command):
    stub_check_call = mocker.patch(
        'certbot_dns_auth.dns01_auth.command.check_call')

    run(command)

    stub_check_call.assert_called_once_with(['/bin/sh', '-c', command])
