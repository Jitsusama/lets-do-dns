"""Test the time delay module."""

from lets_do_dns.acme_dns_auth.time_delay import sleep


def test_sleep_calls_time_sleep(mocker):
    stub_sleep = mocker.patch(
        'lets_do_dns.acme_dns_auth.time_delay.time.sleep')

    sleep(2)

    stub_sleep.assert_called_once_with(2)
