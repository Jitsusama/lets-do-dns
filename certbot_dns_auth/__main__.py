"""Called when run as an executable."""

import os
import sys
from certbot_dns_auth.arguments import Arguments
from certbot_dns_auth.authenticate import Authenticate
from certbot_dns_auth.environment import Environment
from certbot_dns_auth.errors import RequiredInputMissing


def main():
    """Bootstrap the application."""
    arguments = Arguments(sys.argv)
    try:
        Environment(os.environ)
    except RequiredInputMissing:
        sys.exit(2)
    authentication = Authenticate(os.environ, arguments)
    sys.exit(authentication.perform())


if __name__ == '__main__':
    main()
