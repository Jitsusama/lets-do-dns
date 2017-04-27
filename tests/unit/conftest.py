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
def create_environment(
        do_api_key, do_domain, do_hostname, certbot_auth_token):
    class FakeEnvironment(object):
        def __init__(self):
            self.api_key = do_api_key
            self.domain = do_domain
            self.fqdn = '%s.%s' % (do_hostname, do_domain)
            self.validation_key = certbot_auth_token
            self.record_id = None
            self.post_cmd = None

    return FakeEnvironment()


@pytest.fixture()
def delete_environment(create_environment):
    def updated_environment(record_id):
        create_environment.record_id = record_id
        return create_environment

    return updated_environment


@pytest.fixture()
def fake_record(do_api_key, do_domain, do_hostname):
    class FakeRecord(object):
        def __init__(self, api_key=do_api_key, domain=do_domain,
                     hostname=do_hostname):
            self.api_key = api_key
            self.domain = domain
            self.hostname = hostname
            self.number = None

        def create(self):
            pass

    return FakeRecord()


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

        @staticmethod
        def json():
            return None

        @property
        def request(self):
            class Method(object):
                def __init__(self):
                    self.method = 'DELETE'
            return Method()

    return FakeRequestsResponse
