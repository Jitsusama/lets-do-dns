"""Called when run as an executable."""

import os
import sys

from lets_do_dns.acme_dns_auth.authenticate import Authenticate
from lets_do_dns.arguments import Arguments
from lets_do_dns.environment import Environment
from lets_do_dns.errors import InputError, HookError
from lets_do_dns.printer import stderr


def main():
    """Bootstrap the application."""
    try:
        Arguments(sys.argv)
        environment = Environment(os.environ)
        authentication = Authenticate(environment)
        authentication_result = authentication.perform()

    except InputError as exception:
        _handle_exception(exception)

    except HookError as exception:
        _handle_exception(exception)

    else:
        sys.exit(authentication_result)


def _handle_exception(exception):
    exception_message = str(exception)
    stderr(exception_message)
    sys.exit(2)


if __name__ == '__main__':
    main()
