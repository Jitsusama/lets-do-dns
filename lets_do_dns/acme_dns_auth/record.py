"""DNS Record."""

from lets_do_dns.printer import stdout
from lets_do_dns.do_domain.resource import Resource


class Record(object):
    """Represent a DNS record and proxy operations to a handler."""

    def __init__(self, api_key, domain, hostname):
        self._number = None
        self.domain = domain
        self.hostname = hostname
        self.api_key = api_key

    def create(self, value):
        """Create this record on DNS provider with the supplied value."""
        resource = Resource(self, value)
        resource.create()
        self._number = resource.__int__()

    def delete(self):
        """Delete this record with DNS provider."""
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
