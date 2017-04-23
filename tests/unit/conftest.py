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
        'DO_APIKEY': env.key,
        'DO_DOMAIN': env.domain,
        'CERTBOT_DOMAIN': '%s.%s' % (env.hostname, env.domain),
        'CERTBOT_VALIDATION': env.auth_token
    }


@pytest.fixture()
def delete_environment(create_environment):
    def updated_environment(record_id):
        create_environment.update({
            'CERTBOT_AUTH_OUTPUT': record_id})
        return create_environment

    return updated_environment


@pytest.fixture()
def fake_record(env):
    class FakeRecord(object):
        def __init__(self, api_key=env.key, domain=env.domain,
                     hostname=env.hostname):
            self.api_key = api_key
            self.domain = domain
            self.hostname = hostname
            self.number = None

        def create(self):
            pass

    return FakeRecord()


@pytest.fixture()
def fake_requests_post_response(env):
    class FakeRequestsResponse(object):
        def __init__(self, status_code):
            self.id = None
            self.status_code = status_code
            self.url = ('https://api.digitalocean.com/v2/domains/'
                        '%s/records' % env.domain)

        @property
        def ok(self):
            return self.status_code < 400

        def json(self):
            return {
                'domain_record': {
                    'id': self.id, 'type': 'TXT',
                    'name': env.hostname,
                    'data': env.auth_token, 'priority': None,
                    'port': None, 'weight': None
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
def fake_requests_delete_response(env):
    class FakeRequestsResponse(object):
        def __init__(self, status_code, record_id):
            self.status_code = status_code
            self.url = ('https://api.digitalocean.com/v2/domains/'
                        '%s/records/%s' % (env.domain, record_id))

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
