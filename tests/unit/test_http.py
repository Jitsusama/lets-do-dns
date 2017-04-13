from do_record.http import create
from mock import call
import pytest

class StubRecord(object):
    def __init__(self, api_key, domain, hostname):
        self.api_key = api_key
        self.domain = domain
        self.hostname = hostname


def test_create_calls_correct_uri(
        mocker, api_key, domain, hostname, auth_token):
    fake_requests = mocker.patch('do_record.http.requests')
    stub_record = StubRecord(api_key, domain, hostname)

    create(stub_record, auth_token)

    do_record_put_uri = (
        'https://api.digitalocean.com/v2/domains/grrbrr.ca/%s' % hostname)
    call_put_properly = [call.put(do_record_put_uri)]

    fake_requests.assert_has_calls(call_put_properly)
