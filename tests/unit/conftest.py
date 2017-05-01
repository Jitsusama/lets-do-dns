import pytest


@pytest.fixture
def do_auth_header(do_api_key):
    return {'Authorization': 'Bearer %s' % do_api_key}


@pytest.fixture
def do_api_key():
    return 'unit-test-api-key'


@pytest.fixture
def do_domain():
    return 'grrbrr.ca'


@pytest.fixture
def do_hostname():
    return 'unit-test-ssl-host'


@pytest.fixture
def certbot_auth_token():
    return 'unit-test-auth-token'


@pytest.fixture()
def fake_requests_post_response(
        do_domain, do_hostname, certbot_auth_token):
    class FakeRequestsResponse(object):
        def __init__(self, status_code):
            self.id = None
            self.status_code = status_code
            self.url = ('https://api.digitalocean.com/v2/domains/'
                        '%s/records' % do_domain)

        @property
        def ok(self):
            return self.status_code < 400

        def json(self):
            return {
                'domain_record': {
                    'id': self.id,
                    'type': 'TXT',
                    'name': do_hostname,
                    'data': certbot_auth_token,
                    'priority': None,
                    'port': None,
                    'weight': None
                },
                'message': ''}

        @property
        def request(self):
            class Method(object):
                def __init__(self):
                    self.method = 'POST'
            return Method()

    return FakeRequestsResponse


@pytest.fixture()
def fake_requests_delete_response(do_domain):
    class FakeRequestsResponse(object):
        def __init__(self, status_code, record_id):
            self.status_code = status_code
            self.url = ('https://api.digitalocean.com/v2/domains/'
                        '%s/records/%s' % (do_domain, record_id))

        @property
        def ok(self):
            return self.status_code < 400

        @property
        def request(self):
            class Method(object):
                def __init__(self):
                    self.method = 'DELETE'
            return Method()

    return FakeRequestsResponse
