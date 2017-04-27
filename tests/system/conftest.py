import os
import pytest
from requests import post


@pytest.fixture(autouse=True)
def os_environ_reset():
    """Reset os.environ in between test runs."""
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def do_record_id(create_response):
    return create_response.json()['domain_record']['id']


@pytest.fixture
def create_response(
        do_base_uri, do_auth_header, do_domain, do_hostname, request):
    return post(
        '%s/%s/records' % (do_base_uri, do_domain),
        headers=do_auth_header,
        json={'type': 'TXT',
              'name': do_hostname,
              'data': request.function.__name__})


@pytest.fixture
def do_base_uri():
    return 'https://api.digitalocean.com/v2/domains'


@pytest.fixture
def do_auth_header(do_api_key):
    return {'Authorization': 'Bearer %s' % do_api_key}


@pytest.fixture()
def do_api_key():
    file_path = os.path.realpath(__file__)
    directory_path = os.path.dirname(file_path)
    api_key_file = '%s/digital_ocean_api_key.txt' % directory_path

    api_key_file = open(api_key_file, 'r')

    return api_key_file.readline()


@pytest.fixture
def do_domain():
    return 'grrbrr.ca'


@pytest.fixture
def do_hostname():
    return 'test-ssl-host'
