"""Perform letsencrypt's certbot pre/post hook hostname authentication."""

from dns01_auth.authenticate import Authenticate

__all__ = (Authenticate)
