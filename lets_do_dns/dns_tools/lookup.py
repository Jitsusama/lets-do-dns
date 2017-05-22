"""Wrap dnspython package."""
from __future__ import absolute_import

from dns.exception import DNSException
from dns.resolver import query

from lets_do_dns.errors import RecordLookupFailure


def lookup(fqdn):
    """Perform a DNS TXT record lookup against the provided FQDN."""
    try:
        return query(fqdn, 'TXT')
    except DNSException:
        raise RecordLookupFailure()
