"""Called when run as an executable."""

import os
import sys
from certbot_dns_auth.arguments import Arguments
from certbot_dns_auth.authenticate import Authenticate
from certbot_dns_auth.environment import Environment


def main():
    """Bootstrap the application."""
    arguments = Arguments(sys.argv)
    Environment(os.environ)
    authentication = Authenticate(os.environ, arguments)
    sys.exit(authentication.perform())


if __name__ == '__main__':
    main()
