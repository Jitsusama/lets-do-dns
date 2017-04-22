"""Environment Wrapper and Validator."""
from certbot_dns_auth.errors import RequiredInputMissing


class Environment(object):
    """Wraps os.environ and Validates Required Variables Are Present."""

    def __init__(self, environment):
        if environment.get('DO_API_KEY') is None:
            raise RequiredInputMissing
        if environment.get('DO_DOMAIN') is None:
            raise RequiredInputMissing
        if environment.get('CERTBOT_DOMAIN') is None:
            raise RequiredInputMissing
        if environment.get('CERTBOT_VALIDATION') is None:
            raise RequiredInputMissing
