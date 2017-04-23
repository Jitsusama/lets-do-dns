"""Environment Wrapper and Validator."""
from certbot_dns_auth.errors import RequiredInputMissing


class Environment(object):
    """Wraps os.environ and Validates Required Variables Are Present."""

    def __init__(self, environment):
        missing_parameters = list()
        if environment.get('DO_APIKEY') is None:
            missing_parameters.append('DO_APIKEY')
        if environment.get('DO_DOMAIN') is None:
            missing_parameters.append('DO_DOMAIN')
        if environment.get('CERTBOT_DOMAIN') is None:
            missing_parameters.append('CERTBOT_DOMAIN')
        if environment.get('CERTBOT_VALIDATION') is None:
            missing_parameters.append('CERTBOT_VALIDATION')

        if len(missing_parameters) > 1:
            raise RequiredInputMissing(
                'Missing the following required environment variables: '
                '%s and %s' % (', '.join(missing_parameters[:-1]),
                               missing_parameters[-1]))
        elif len(missing_parameters) == 1:
            raise RequiredInputMissing(
                'Missing the following required environment variable: '
                '%s' % missing_parameters[0])
