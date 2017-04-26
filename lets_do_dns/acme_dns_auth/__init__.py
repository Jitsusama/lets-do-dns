"""Perform letsencrypt's certbot pre/post hook hostname authentication."""

from lets_do_dns.acme_dns_auth.authenticate import Authenticate

__all__ = (Authenticate)
