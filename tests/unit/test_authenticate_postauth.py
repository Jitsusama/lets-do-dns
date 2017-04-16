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
