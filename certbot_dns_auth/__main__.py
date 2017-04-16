"""Called when run as an executable."""

import os
import sys
from . import Authenticate


def main():
    """Bootstrap the application."""
    authentication = Authenticate(os.environ)
    sys.exit(authentication.perform())


if __name__ == '__main__':
    main()
