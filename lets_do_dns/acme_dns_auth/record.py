"""DNS Record."""

from lets_do_dns.printer import stdout
from lets_do_dns.acme_dns_auth import dns
from lets_do_dns.do_domain.resource import Resource


class Record(object):
    """Represent a DNS record and proxy operations to a handler."""

    def __init__(self, api_key, domain, hostname):
        self.id = None
        self.domain = domain
        self.hostname = hostname
        self.api_key = api_key

    def create(self, value):
        """Create this record on DNS provider with the supplied value."""
        resource = Resource(self, value)
        resource.create()
        self.id = resource.__int__()

    def delete(self):
        """Delete this record with DNS provider."""
        resource = Resource(self)
        resource.delete()

    def printer(self):
        """Print out record ID."""
        stdout(self.id)

    def exists(self):
        """Verify that the record exists in DNS."""
        fqdn = '{}.{}'.format(self.hostname, self.domain)
        return dns.lookup(fqdn)
