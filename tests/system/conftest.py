import os
import pytest


@pytest.fixture(autouse=True)
def os_environ_reset():
    """Reset os.environ in between test runs."""
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture()
def env(api_key):
    class Environment(object):
        def __init__(self):
            self.key = api_key
            self.auth_header = {'Authorization': 'Bearer %s' % self.key}
            self.auth_token = 'validate-with-thing'
            self.domain = 'grrbrr.ca'
            self.hostname = 'test-ssl-host'
            self.base_uri = 'https://api.digitalocean.com/v2/domains'

    return Environment()


@pytest.fixture()
def api_key():
    file_path = os.path.realpath(__file__)
    directory_path = os.path.dirname(file_path)
    api_key_file = '%s/digital_ocean_api_key.txt' % directory_path

    api_key_file = open(api_key_file, 'r')

    return api_key_file.readline()
