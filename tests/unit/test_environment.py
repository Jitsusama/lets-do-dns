from certbot_dns_auth.environment import Environment
from certbot_dns_auth.errors import RequiredInputMissing
import pytest


@pytest.mark.parametrize(
    'environment',
    [{},
     {'DO_DOMAIN': 'b', 'CERTBOT_DOMAIN': 'c', 'CERTBOT_VALIDATION': 'd'},
     {'DO_APIKEY': 'a', 'CERTBOT_DOMAIN': 'c', 'CERTBOT_VALIDATION': 'd'},
     {'DO_APIKEY': 'a', 'DO_DOMAIN': 'b', 'CERTBOT_VALIDATION': 'd'},
     {'DO_APIKEY': 'a', 'DO_DOMAIN': 'b', 'CERTBOT_DOMAIN': 'c'}])
def test_missing_required_argument_causes_required_parameter_exception(
        environment):
    with pytest.raises(RequiredInputMissing):
        Environment(environment)


def test_does_not_raise_exception_with_required_arguments_present():
    environment = {'DO_APIKEY': 'a',
                   'DO_DOMAIN': 'b',
                   'CERTBOT_DOMAIN': 'c',
                   'CERTBOT_VALIDATION': 'd'}

    Environment(environment)


@pytest.mark.parametrize(
    'environment,message_segment',
    [({},
      ': DO_APIKEY, DO_DOMAIN, CERTBOT_DOMAIN and CERTBOT_VALIDATION'),
     ({'DO_DOMAIN': 'b', 'CERTBOT_DOMAIN': 'c', 'CERTBOT_VALIDATION': 'd'},
      ': DO_APIKEY'),
     ({'DO_APIKEY': 'a', 'CERTBOT_DOMAIN': 'c', 'CERTBOT_VALIDATION': 'd'},
      ': DO_DOMAIN'),
     ({'DO_APIKEY': 'a', 'DO_DOMAIN': 'b', 'CERTBOT_VALIDATION': 'd'},
      ': CERTBOT_DOMAIN'),
     ({'DO_APIKEY': 'a', 'DO_DOMAIN': 'b', 'CERTBOT_DOMAIN': 'c'},
      ': CERTBOT_VALIDATION')])
def test_passes_missing_variables_to_exception_message(
        environment, message_segment):
    with pytest.raises(RequiredInputMissing) as exception:
        Environment(environment)

    assert str(exception).find(message_segment) > 0
