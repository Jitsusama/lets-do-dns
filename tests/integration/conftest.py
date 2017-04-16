import pytest


@pytest.fixture()
def env():
    class Environment(object):
        def __init__(self):
            self.key = 'nobody-knows'
            self.auth_header = {'Authorization': 'Bearer %s' % self.key}
            self.auth_token = 'validate-with-thing'
            self.domain = 'grrbrr.ca'
            self.hostname = 'test-integration-ssl-host'

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
def delete_environment(create_environment):
    def updated_environment(record_id):
        create_environment.update({
            'CERTBOT_AUTH_OUTPUT': record_id})
        return create_environment

    return updated_environment


@pytest.fixture()
def fake_requests_response(env):
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

    return FakeRequestsResponse
