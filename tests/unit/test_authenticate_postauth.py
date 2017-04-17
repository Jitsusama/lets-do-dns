"""Test the DigitalOcean backed ACME DNS Authentication Class."""

from certbot_dns_auth import Authenticate
from mock import call


def test_triggers_record_deletion_after_initialization(
        mocker, env, delete_environment):
    stub_record = mocker.patch('certbot_dns_auth.authenticate.Record')

    authentication = Authenticate(environment=delete_environment(918232))
    authentication.perform()

    initialize_then_delete = [
        call(env.key, env.domain, env.hostname),
        call().delete(918232)]
    stub_record.assert_has_calls(initialize_then_delete)


def test_runs_postcmd_program(
        mocker, delete_environment):
    mocker.patch('certbot_dns_auth.authenticate.Record')
    stub_run = mocker.patch('certbot_dns_auth.authenticate.run')

    delete_environment = delete_environment(1)
    delete_environment.update({'LETS_DO_POSTCMD': 'test-program'})

    authentication = Authenticate(environment=delete_environment)
    authentication.perform()

    stub_run.assert_called_once_with('test-program')
