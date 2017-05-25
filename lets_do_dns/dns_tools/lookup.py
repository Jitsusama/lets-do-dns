"""Wrap dnspython package."""

from dns.exception import DNSException
from dns.resolver import query

from lets_do_dns.errors import RecordLookupError


def lookup(fqdn):
    """Perform a DNS TXT record lookup against the provided FQDN."""
    try:
        return query(fqdn, 'TXT')
    except DNSException as exception:
        raise RecordLookupError(exception)
