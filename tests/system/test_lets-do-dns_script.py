import os
import subprocess
import pytest
from requests import get, delete, post

# ATTENTION: Look at conftest.py for py.test fixture definitions.


def test_pre_authentication_hook(env):
    os.environ.update({
        'DO_API_KEY': env.key,
        'DO_DOMAIN': env.domain,
        'CERTBOT_DOMAIN': '%s.%s' % (env.hostname, env.domain),
        'CERTBOT_VALIDATION': env.auth_token,
    })

    record_id = subprocess.check_output('lets-do-dns')

    assert int(record_id) > 0

    request_uri = '%s/%s/records/%s' % (
        env.base_uri, env.domain, record_id)
    response = get(request_uri, headers=env.auth_header)
    record_data = response.json()['domain_record']

    assert (record_data['type'] == 'TXT' and
            record_data['name'] == env.hostname and
            record_data['data'] == env.auth_token)

    delete(request_uri, headers=env.auth_header)


def test_post_authentication_hook_without_post_command(env):
    create_response = post(
        '%s/%s/records' % (env.base_uri, env.domain),
        headers=env.auth_header,
        json={'type': 'TXT',
              'name': env.hostname,
              'data': env.auth_token})
    record_id = create_response.json()['domain_record']['id']

    os.environ.update({
        'DO_API_KEY': env.key,
        'DO_DOMAIN': env.domain,
        'CERTBOT_DOMAIN': '%s.%s' % (env.hostname, env.domain),
        'CERTBOT_VALIDATION': env.auth_token,
        'CERTBOT_AUTH_OUTPUT': str(record_id)
    })

    subprocess.check_call('lets-do-dns')

    request_uri = '%s/%s/records/%s' % (
        env.base_uri, env.domain, record_id)
    get_response = get(request_uri, headers=env.auth_header)

    assert get_response.status_code == 404


def test_post_authentication_hook_with_post_command(env):
    create_response = post(
        '%s/%s/records' % (env.base_uri, env.domain),
        headers=env.auth_header,
        json={'type': 'TXT',
              'name': env.hostname,
              'data': env.auth_token})
    record_id = create_response.json()['domain_record']['id']

    os.environ.update({
        'DO_API_KEY': env.key,
        'DO_DOMAIN': env.domain,
        'CERTBOT_DOMAIN': '%s.%s' % (env.hostname, env.domain),
        'CERTBOT_VALIDATION': env.auth_token,
        'CERTBOT_AUTH_OUTPUT': str(record_id),
        'LETS_DO_POSTCMD': 'echo hello',
    })

    postcmd_output = subprocess.check_output('lets-do-dns')

    request_uri = '%s/%s/records/%s' % (
        env.base_uri, env.domain, record_id)
    get_response = get(request_uri, headers=env.auth_header)

    assert (get_response.status_code == 404 and
            postcmd_output == 'hello\n')


def test_help_command():
    help_output = subprocess.check_output(['lets-do-dns', '--help'])

    assert help_output.find('lets-do-dns') >= 0


def test_missing_required_environment_variables_exits_properly(capsys):
    with pytest.raises(subprocess.CalledProcessError) as exception:
        subprocess.check_call('lets-do-dns')

    _, error_output = capsys.readouterr()

    assert (exception.value.returncode == 2 and
            error_output.find('missing') > 0)
