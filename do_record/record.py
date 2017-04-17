"""DigitalOcean DNS Records."""

from do_record import http


class Record(object):
    """Handle DigitalOcean DNS records."""

    def __init__(self, api_key, domain, hostname):
        self._id = None
        self.domain = domain
        self.hostname = hostname
        self.api_key = api_key

    def create(self, value):
        """Create this record on DigitalOcean with the supplied value."""
        self._id = http.create(self, value)
        return self.id

    def delete(self, record_id):
        """Delete this record on DigitalOcean, identified by record_id."""
        http.delete(self, record_id)

    @property
    def id(self):
        return self._id
