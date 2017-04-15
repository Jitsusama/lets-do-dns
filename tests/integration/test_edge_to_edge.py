from acmednsauth.authenticate import Authenticate
import pytest

API_KEY = 'nobody-knows'
AUTH_TOKEN = 'validate-with-thing'
DOMAIN = 'grrbrr.ca'
HOSTNAME = 'test-integration-ssl-host'


@pytest.mark.parametrize('record_id', [987623])
def test_digitalocean_authentication_record_creation(mocker, record_id):
    mocker.patch('do_record.http.requests.post',
                 return_value=FakePost(record_id))
    mocker.patch('do_record.http.requests.delete',
                 return_value=FakeDelete())
    stub_printer = mocker.patch('acmednsauth.authenticate.printer')

    fake_create_environment = {
        'DO_API_KEY': API_KEY,
        'DO_DOMAIN': DOMAIN,
        'CERTBOT_DOMAIN': '%s.%s' % (HOSTNAME, DOMAIN),
        'CERTBOT_VALIDATION': AUTH_TOKEN,
    }

    Authenticate(environment=fake_create_environment)

    stub_printer.assert_called_once_with(record_id)


class FakePost(object):
    def __init__(self, record_id):
        self.id = record_id
        self.status_code = 201

    def json(self):
        return {
            'domain_record': {
                'id': self.id, 'type': 'TXT', 'name': HOSTNAME,
                'data': AUTH_TOKEN, 'priority': None, 'port': None,
                'weight': None}}


class FakeDelete(object):
    def __init__(self):
        self.status_code = 204
