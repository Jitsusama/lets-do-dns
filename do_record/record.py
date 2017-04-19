"""DigitalOcean DNS Records."""

from certbot_dns_auth.printer import printer
from do_record import http


class Record(object):
    """Handle DigitalOcean DNS records."""

    def __init__(self, api_key, domain, hostname):
        self._number = None
        self.domain = domain
        self.hostname = hostname
        self.api_key = api_key

    def create(self, value):
        """Create this record on DigitalOcean with the supplied value."""
        resource = http.Resource(self, value)
        resource.create()
        self._number = resource.__int__()

    def delete(self):
        """Delete this record on DigitalOcean."""
        http.delete(self)

    def printer(self):
        """Print out record ID number."""
        printer(self.number)

    @property
    def number(self):
        """Record ID number."""
        return self._number

    @number.setter
    def number(self, value):
        self._number = value
