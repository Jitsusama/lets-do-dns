"""Called when run as an executable."""

import os
import sys
from certbot_dns_auth.arguments import Arguments
from certbot_dns_auth.authenticate import Authenticate


def main():
    """Bootstrap the application."""
    arguments = Arguments(sys.argv)
    authentication = Authenticate(os.environ, arguments)
    sys.exit(authentication.perform())


if __name__ == '__main__':
    main()
