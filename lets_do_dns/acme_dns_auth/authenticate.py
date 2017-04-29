"""letsencrypt's certbot Authentication Logic."""

from lets_do_dns.acme_dns_auth.record import Record
from lets_do_dns.acme_dns_auth.command import run
from lets_do_dns.acme_dns_auth.time_delay import sleep


class Authenticate(object):
    """Handle letsencrypt DNS certificate identity authentication."""

    def __init__(self, environment):
        self._env = environment
        self._record = self._init_record()

    def perform(self):
        """Execute the authentication logic."""
        if self._in_authentication_hook_stage:
            self._create_record()
            self._print_record_id()
            self._delay_finish()

        elif self._in_cleanup_hook_stage:
            self._delete_record()
            self._run_post_cmd()

        return 0

    @property
    def _in_authentication_hook_stage(self):
        return self._env.record_id is None

    @property
    def _in_cleanup_hook_stage(self):
        return self._env.record_id is not None

    def _delete_record(self):
        self._record.id = self._env.record_id
        self._record.delete()

    def _run_post_cmd(self):
        if self._env.post_cmd:
            run(self._env.post_cmd)

    def _create_record(self):
        self._record.create(self._env.validation_key)

    def _print_record_id(self):
        self._record.printer()

    def _init_record(self):
        hostname = self._parse_hostname()
        record = Record(self._env.api_key, self._env.domain, hostname)
        return record

    def _parse_hostname(self):
        domain_suffix = '.' + self._env.domain
        domain_start = self._env.fqdn.rfind(domain_suffix)

        cert_hostname = self._env.fqdn[0:domain_start]
        auth_hostname = '_acme-challenge.%s' % cert_hostname

        return auth_hostname

    @staticmethod
    def _delay_finish():
        sleep(2)
