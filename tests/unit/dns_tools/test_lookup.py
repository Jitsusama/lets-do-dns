"""Tests the lets_do_dns.dns_tools.lookup.py module."""

from dns.resolver import NXDOMAIN, NoAnswer
import pytest
from lets_do_dns.errors import RecordLookupError

from lets_do_dns.dns_tools.lookup import lookup


def test_properly_calls_query(mocker):
    mock_query = mocker.patch('lets_do_dns.dns_tools.lookup.query')

    lookup('stub-host.stub-domain')

    mock_query.assert_called_once_with('stub-host.stub-domain', 'TXT')


def test_returns_result_of_query(mocker):
    mocker.patch(
        'lets_do_dns.dns_tools.lookup.query',
        return_value='stub-result')

    lookup_result = lookup('stub-host.stub-domain')

    assert lookup_result == 'stub-result'


@pytest.mark.parametrize('dns_raises_this', [NoAnswer, NXDOMAIN])
def test_raises_error_on_dns_error(mocker, dns_raises_this):
    mocker.patch(
        'lets_do_dns.dns_tools.lookup.query',
        side_effect=dns_raises_this)

    with pytest.raises(RecordLookupError):
        lookup('stub-host.stub-domain')


def test_passes_dns_exception_to_raised_error(mocker):
    stub_no_answer = NoAnswer()
    mocker.patch('lets_do_dns.dns_tools.lookup.query',
                 side_effect=stub_no_answer)

    mock_lookup_error = mocker.patch(
        'lets_do_dns.dns_tools.lookup.RecordLookupError',
        autospec=True, return_value=RecordLookupError)

    with pytest.raises(RecordLookupError):
        lookup('stub-host.stub-domain')

    mock_lookup_error.assert_called_once_with(stub_no_answer)
