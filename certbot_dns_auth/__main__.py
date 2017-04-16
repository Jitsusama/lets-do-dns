import os
import sys
from . import Authenticate


def main():
    authentication = Authenticate(os.environ)
    sys.exit(authentication.perform())
