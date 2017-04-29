import pytest
from mock import ANY

from lets_do_dns.do_domain.resource import Resource

# ATTENTION: Look at conftest.py for py.test fixture definitions.


def test_calls_delete(mocker, fake_record):
    stub_requests = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete')
    fake_record.number = 2322346

    resource = Resource(fake_record)
    resource.delete()

    stub_requests.assert_called_once()


@pytest.mark.parametrize('record_id', [82227342, 2342552])
def test_calls_correct_uri(mocker, do_domain, fake_record, record_id):
    stub_requests = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete')
    fake_record.id = record_id

    resource = Resource(fake_record)
    resource.delete()

    record_delete_uri = (
        'https://api.digitalocean.com/v2/domains/%s/records/%s' % (
            do_domain, record_id))

    stub_requests.assert_called_once_with(record_delete_uri, headers=ANY)


@pytest.mark.parametrize('record_id', [4323422, 1231123])
def test_passes_authorization_header(
        mocker, do_auth_header, fake_record, record_id):
    stub_requests = mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete')
    fake_record.number = record_id

    resource = Resource(fake_record)
    resource.delete()

    stub_requests.assert_called_once_with(ANY, headers=do_auth_header)


@pytest.mark.parametrize('record_id', [77238234, 235223])
def test_calls_response_with_delete_response(
        mocker, fake_record, record_id):
    mocker.patch(
        'lets_do_dns.do_domain.resource.requests.delete',
        return_value=record_id)
    stub_response = mocker.patch(
        'lets_do_dns.do_domain.resource.Response')
    fake_record.number = record_id

    resource = Resource(fake_record)
    resource.delete()
    resource.__int__()

    stub_response.assert_called_with(record_id)
