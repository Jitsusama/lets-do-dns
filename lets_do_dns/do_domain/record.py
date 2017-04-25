"""DigitalOcean DNS Records."""

from lets_do_dns.printer import stdout
from lets_do_dns.do_domain.resource import Resource


class Record(object):
    """Handle DigitalOcean DNS records."""

    def __init__(self, api_key, domain, hostname):
        self._number = None
        self.domain = domain
        self.hostname = hostname
        self.api_key = api_key

    def create(self, value):
        """Create this record on DigitalOcean with the supplied value."""
        resource = Resource(self, value)
        resource.create()
        self._number = resource.__int__()

    def delete(self):
        """Delete this record on DigitalOcean."""
        resource = Resource(self)
        resource.delete()

    def printer(self):
        """Print out record ID number."""
        stdout(self.number)

    @property
    def number(self):
        """Record ID number."""
        return self._number

    @number.setter
    def number(self, value):
        self._number = value
