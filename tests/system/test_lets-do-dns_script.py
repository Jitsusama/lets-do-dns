import os
import subprocess
from requests import get, delete


def test_pre_authentication_hook(capsys, env):
    os.environ.update({
        'DO_API_KEY': env.key,
        'DO_DOMAIN': env.domain,
        'CERTBOT_DOMAIN': '%s.%s' % (env.hostname, env.domain),
        'CERTBOT_VALIDATION': env.auth_token,
    })

    subprocess.check_call('lets-do-dns')

    record_id, _ = capsys.readouterr()

    assert int(record_id) > 0

    request_uri = '%s/%s/records/%s' % (
        env.base_uri, env.domain, record_id)
    response = get(request_uri, headers=env.auth_header)
    record_data = response.json()['domain_record']

    assert (record_data['type'] == 'TXT' and
            record_data['name'] == env.hostname and
            record_data['data'] == env.auth_token)

    delete(request_uri, headers=env.auth_header)
