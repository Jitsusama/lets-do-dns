import pytest

from lets_do_dns.errors import (
    AuthenticationFailure, RecordCreationFailure, RecordLookupFailure)


@pytest.mark.parametrize(
    'child_exception', [RecordCreationFailure, RecordLookupFailure])
def test_authentication_errors_inherit_from_base_error(
        child_exception):
    assert issubclass(child_exception, AuthenticationFailure)
