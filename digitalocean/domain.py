from digitalocean import http


class Record(object):
    """Handle DigitalOcean DNS records."""

    def __init__(self, api_key, domain, hostname):
        pass

    def create(self, value):
        return http.create()
