"""Environment Wrapper and Validator."""
from lets_do_dns.errors import InputError


class Environment(object):
    """Validates and Stores Desired Environment Variables."""

    def __init__(self, environment):
        self._environ = environment
        self._missing_parameters = list()

        # Required Parameters
        self.api_key = self._obtain_parameter('DO_APIKEY')
        self.domain = self._obtain_parameter('DO_DOMAIN')
        self.fqdn = self._obtain_parameter('CERTBOT_DOMAIN')
        self.validation_key = self._obtain_parameter('CERTBOT_VALIDATION')

        # "Optional" Parameters
        self.record_id = self._obtain_parameter('CERTBOT_AUTH_OUTPUT')
        self.post_cmd = self._obtain_parameter('LETS_DO_POSTCMD')

        self._validate_environment()

    def _obtain_parameter(self, key):
        value = self._environ.get(key)

        optional_parameters = [
            'CERTBOT_AUTH_OUTPUT',
            'LETS_DO_POSTCMD']

        if value is None and key not in optional_parameters:
            self._missing_parameters.append(key)

        return value

    def _validate_environment(self):
        exception_message = self._generate_exception_message()

        if exception_message:
            raise InputError(exception_message)

    def _generate_exception_message(self):
        if len(self._missing_parameters) == 1:
            return self._missing_parameters[0]

        if len(self._missing_parameters) > 1:
            return '{} and {}'.format(
                ', '.join(self._missing_parameters[:-1]),
                self._missing_parameters[-1])
