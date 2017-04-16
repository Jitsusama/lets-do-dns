"""DigitalOcean DNS Records."""

from do_record import http


class Record(object):
    """Handle DigitalOcean DNS records."""

    def __init__(self, api_key, domain, hostname):
        self.api_key = api_key
        self.domain = domain
        self.hostname = hostname

    def create(self, value):
        """Create this record on DigitalOcean with the supplied value."""
        return http.create(self, value)
