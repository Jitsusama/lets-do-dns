import pytest
from dns.resolver import NXDOMAIN, NoAnswer

from lets_do_dns.acme_dns_auth.dns import lookup
from lets_do_dns.errors import RecordLookupFailure


def test_properly_calls_lookup(mocker):
    stub_query = mocker.patch('lets_do_dns.acme_dns_auth.dns.query')

    lookup('stub-hostname.stub-domain')

    stub_query.assert_called_once_with('stub-hostname.stub-domain', 'TXT')


def test_returns_result_of_lookup(mocker):
    mocker.patch(
        'lets_do_dns.acme_dns_auth.dns.query',
        return_value='stub-result')

    assert lookup('stub-hostname.stub-domain') == 'stub-result'


@pytest.mark.parametrize('dns_raises_this', [NoAnswer, NXDOMAIN])
def test_raises_error_on_dns_error(mocker, dns_raises_this):
    mocker.patch(
        'lets_do_dns.acme_dns_auth.dns.query',
        side_effect=dns_raises_this)

    with pytest.raises(RecordLookupFailure):
        lookup('stub-hostname.stub-domain')
