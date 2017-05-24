import pytest

from lets_do_dns.environment import Environment
from lets_do_dns.errors import RequiredInputMissingError


@pytest.mark.parametrize(
    'environment',
    [{},
     {'DO_DOMAIN': 'b', 'CERTBOT_DOMAIN': 'c', 'CERTBOT_VALIDATION': 'd'},
     {'DO_APIKEY': 'a', 'CERTBOT_DOMAIN': 'c', 'CERTBOT_VALIDATION': 'd'},
     {'DO_APIKEY': 'a', 'DO_DOMAIN': 'b', 'CERTBOT_VALIDATION': 'd'},
     {'DO_APIKEY': 'a', 'DO_DOMAIN': 'b', 'CERTBOT_DOMAIN': 'c'}])
def test_missing_required_argument_causes_required_parameter_exception(
        environment):
    with pytest.raises(RequiredInputMissingError):
        Environment(environment)


def test_does_not_raise_exception_with_required_arguments_present():
    stub_environment = {
        'DO_APIKEY': 'a', 'DO_DOMAIN': 'b',
        'CERTBOT_DOMAIN': 'c', 'CERTBOT_VALIDATION': 'd'}

    Environment(stub_environment)


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
    with pytest.raises(RequiredInputMissingError) as exception:
        Environment(environment)

    assert str(exception).find(message_segment) > 0


def test_stores_environment_variables_as_properties():
    stub_environment = {
        'DO_APIKEY': 'a',
        'DO_DOMAIN': 'b',
        'CERTBOT_DOMAIN': 'c',
        'CERTBOT_VALIDATION': 'd',
        'CERTBOT_AUTH_OUTPUT': 'e',
        'LETS_DO_POSTCMD': 'f'}

    mock_environment = Environment(stub_environment)

    assert (mock_environment.api_key == 'a' and
            mock_environment.domain == 'b' and
            mock_environment.fqdn == 'c' and
            mock_environment.validation_key == 'd' and
            mock_environment.record_id == 'e' and
            mock_environment.post_cmd == 'f')
