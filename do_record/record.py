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
        self._number = http.create(self, value)
        return self.number

    def delete(self, record_id=None):
        """Delete this record on DigitalOcean, identified by record_id."""
        if record_id is None:
            record_id = self.number
        http.delete(self, record_id)

    def printer(self):
        printer(self.number)

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        if self.number is None:
            self._number = value
        else:
            raise ValueError(
                'Cannot externally reset a record\'s number identifier.')
