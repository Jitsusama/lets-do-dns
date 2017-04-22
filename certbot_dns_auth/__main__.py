"""Called when run as an executable."""

import os
import sys
from certbot_dns_auth.arguments import Arguments
from certbot_dns_auth.authenticate import Authenticate
from certbot_dns_auth.environment import Environment
from certbot_dns_auth.errors import RequiredInputMissing
from certbot_dns_auth.printer import stdout


def main():
    """Bootstrap the application."""
    arguments = Arguments(sys.argv)

    try:
        Environment(os.environ)
    except RequiredInputMissing as exception:
        _handle_missing_input_exception(exception)

    authentication = Authenticate(os.environ, arguments)
    sys.exit(authentication.perform())


def _handle_missing_input_exception(exception):
    stdout(exception.message)
    sys.exit(2)


if __name__ == '__main__':
    main()
