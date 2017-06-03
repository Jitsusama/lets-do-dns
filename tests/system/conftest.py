try:
    import ConfigParser as configparser
except ImportError:
    import configparser

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


@pytest.fixture(scope='module')
def test_configuration():
    """Read test configuration from :file:`config.ini` file.

    The INI file must have a ``[DEFAULT]`` section containing the following
    parameters:

    *  ``do_api_key``
    *  ``do_domain``
    *  ``do_hostname``
    """
    file_path = os.path.realpath(__file__)
    directory_path = os.path.dirname(file_path)
    config_file = '%s/config.ini' % directory_path

    config = configparser.ConfigParser()
    config.read(config_file)

    return config


@pytest.fixture
def create_response(
        do_base_uri, do_auth_header, do_domain, do_hostname, request):
    return post(
        '%s/%s/records' % (do_base_uri, do_domain),
        headers=do_auth_header,
        json={'type': 'TXT',
              'name': do_hostname,
              'data': request.function.__name__})


@pytest.fixture()
def do_api_key(test_configuration):
    return test_configuration.get('DEFAULT', 'do_api_key')


@pytest.fixture
def do_auth_header(do_api_key):
    return {'Authorization': 'Bearer %s' % do_api_key}


@pytest.fixture
def do_base_uri():
    return 'https://api.digitalocean.com/v2/domains'


@pytest.fixture
def do_domain(test_configuration):
    return test_configuration.get('DEFAULT', 'do_domain')


@pytest.fixture
def do_hostname(test_configuration):
    return test_configuration.get('DEFAULT', 'do_hostname')


@pytest.fixture
def do_record_id(create_response):
    return create_response.json()['domain_record']['id']
