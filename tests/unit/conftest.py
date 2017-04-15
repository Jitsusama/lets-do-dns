import pytest


@pytest.fixture()
def env():
    class Environment(object):
        def __init__(self):
            self.key = 'shhhhhhh'
            self.auth_header = {'Authorization': 'Bearer %s' % self.key}
            self.auth_token = 'validate-with-another'
            self.domain = 'grrbrr.ca'
            self.hostname = 'test-ssl-hostie'

    return Environment()


@pytest.fixture()
def create_environment(env):
    return {
        'DO_API_KEY': env.key,
        'DO_DOMAIN': env.domain,
        'CERTBOT_DOMAIN': '%s.%s' % (env.hostname, env.domain),
        'CERTBOT_VALIDATION': env.auth_token
    }


@pytest.fixture()
def fake_record(env):
    class FakeRecord(object):
        def __init__(self, api_key=env.key, domain=env.domain,
                     hostname=env.hostname):
            self.api_key = api_key
            self.domain = domain
            self.hostname = hostname

        @staticmethod
        def create(self): return 123456

    return FakeRecord


@pytest.fixture()
def fake_requests_response(env):
    class FakeRequestsResponse(object):
        def __init__(self, status_code):
            self.id = None
            self.status_code = status_code
            self.url = 'https://api.digitalocean.com/v2/domains/%s/%s' % (
                env.domain, env.hostname)

        @property
        def ok(self): return self.status_code < 400

        def json(self):
            return {
                'domain_record': {
                    'id': self.id, 'type': 'TXT',
                    'name': env.hostname,
                    'data': env.auth_token, 'priority': None,
                    'port': None, 'weight': None
                },
                'message': ''}

    return FakeRequestsResponse
