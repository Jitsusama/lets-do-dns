"""Perform letsencrypt's certbot pre/post hook hostname authentication."""

from acme_dns_auth.authenticate import Authenticate

__all__ = (Authenticate)
