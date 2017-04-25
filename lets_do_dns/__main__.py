"""Called when run as an executable."""

import os
import sys

from lets_do_dns.arguments import Arguments
from lets_do_dns.environment import Environment
from lets_do_dns.errors import RequiredInputMissing
from lets_do_dns.printer import stderr
from lets_do_dns.dns01_auth import Authenticate


def main():
    """Bootstrap the application."""
    arguments = Arguments(sys.argv)

    try:
        environment = Environment(os.environ)
    except RequiredInputMissing as exception:
        _handle_missing_input_exception(exception)
    else:
        authentication = Authenticate(environment, arguments)
        sys.exit(authentication.perform())


def _handle_missing_input_exception(exception):
    stderr(exception.message)
    sys.exit(2)


if __name__ == '__main__':
    main()