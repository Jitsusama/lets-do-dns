"""Validates CLI Arguments."""

import argparse


class Arguments(object):
    """Parses Passed Arguments."""

    def __init__(self, arguments):
        parser = argparse.ArgumentParser(
            description=self._description, epilog=self._epilog)
        parser.parse_args(arguments[1:])

    @property
    def _description(self):
        return '''\
Perform ACME DNS01 authentication for the EFF's certbot program.

The DNS01 authentication record will be created via DigitalOcean's
REST API.'''

    @property
    def _epilog(self):
        return '''\
This program requires the presence of the CERTBOT_DOMAIN and
CERTBOT_VALIDATION environment variables. These should be supplied by
the certbot program when this program is called via its
--manual-auth-hook or --manual-cleanup-hook arguments.

This program also requires the presence of the DO_APIKEY and
DO_DOMAIN environment variables. These have to be provided via the
environment that certbot is executed from.

DO_APIKEY refers to a DigitalOcean API key generated through its API
control panel. This key should have read and write access to your
DigitalOcean account.

DO_DOMAIN refers to which domain under your DigitalOcean account will
function as the root of the certbot SSL certificate authentication
request.'''
