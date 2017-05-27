"""Tests the lets_do_dns.acme_dns_auth.time_delay.py module."""

from lets_do_dns.acme_dns_auth.time_delay import sleep


def test_sleep_calls_time_sleep(mocker):
    mock_sleep = mocker.patch(
        'lets_do_dns.acme_dns_auth.time_delay.time.sleep')

    sleep(2)

    mock_sleep.assert_called_once_with(2)
