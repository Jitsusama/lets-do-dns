from do_record.http import create
from mock import call
import pytest


def test_create_calls_correct_uri(
        mocker, api_key, domain, hostname, auth_token):
    stub_requests = mocker.patch('do_record.http.requests')

    create(api_key, domain, hostname, auth_token)

    do_record_put_uri = (
        'https://api.digitalocean.com/v2/domains/grrbrr.ca/%s' % hostname)
    call_put_properly = [call.put(do_record_put_uri)]

    stub_requests.assert_has_calls(call_put_properly)
