import os
import subprocess
import pytest
from requests import get, delete, post

# ATTENTION: Look at conftest.py for py.test fixture definitions.


def test_pre_authentication_hook(
        do_base_uri, do_auth_header, do_api_key, do_domain, do_hostname):
    os.environ.update({
        'DO_APIKEY': do_api_key,
        'DO_DOMAIN': do_domain,
        'CERTBOT_DOMAIN':
            '%s.%s' % (do_hostname, do_domain),
        'CERTBOT_VALIDATION':
            'test_pre_authentication_hook',
    })

    program_output = subprocess.check_output('lets-do-dns')
    record_id = program_output.decode()

    request_uri = '%s/%s/records/%s' % (
        do_base_uri, do_domain, record_id)

    try:
        response = get(request_uri, headers=do_auth_header)
        record_data = response.json()['domain_record']
        expected_hostname = '_acme-challenge.%s' % do_hostname

        assert (record_data['type'] == 'TXT' and
                record_data['name'] == expected_hostname and
                record_data['data'] == 'test_pre_authentication_hook')

    finally:  # we always want to delete the created record.
        delete(request_uri, headers=do_auth_header)


def test_post_authentication_hook_without_post_command(
        do_base_uri, do_auth_header, do_api_key, do_domain, do_hostname,
        do_record_id):
    os.environ.update({
        'DO_APIKEY': do_api_key,
        'DO_DOMAIN': do_domain,
        'CERTBOT_DOMAIN':
            '%s.%s' % (do_hostname, do_domain),
        'CERTBOT_VALIDATION':
            'test_post_authentication_hook_without_post_command',
        'CERTBOT_AUTH_OUTPUT':
            str(do_record_id)
    })

    subprocess.check_call('lets-do-dns')

    request_uri = '%s/%s/records/%s' % (
        do_base_uri, do_domain, do_record_id)
    get_response = get(request_uri, headers=do_auth_header)

    assert get_response.status_code == 404


def test_post_authentication_hook_with_post_command(
        do_base_uri, do_auth_header, do_api_key, do_domain, do_hostname,
        do_record_id):
    os.environ.update({
        'DO_APIKEY': do_api_key,
        'DO_DOMAIN': do_domain,
        'LETS_DO_POSTCMD': 'echo hello',
        'CERTBOT_DOMAIN':
            '%s.%s' % (do_hostname, do_domain),
        'CERTBOT_VALIDATION':
            'test_post_authentication_hook_with_post_command',
        'CERTBOT_AUTH_OUTPUT':
            str(do_record_id),
    })

    postcmd_output = subprocess.check_output('lets-do-dns')

    request_uri = '%s/%s/records/%s' % (
        do_base_uri, do_domain, do_record_id)
    get_response = get(request_uri, headers=do_auth_header)

    assert (get_response.status_code == 404 and
            postcmd_output.decode() == 'hello\n')


def test_help_command():
    help_output = subprocess.check_output(['lets-do-dns', '--help'])

    assert str(help_output).find('lets-do-dns') >= 0


def test_missing_required_environment_variables_exits_properly():
    with pytest.raises(subprocess.CalledProcessError) as exception:
        subprocess.check_call('lets-do-dns')

    assert exception.value.returncode == 2
