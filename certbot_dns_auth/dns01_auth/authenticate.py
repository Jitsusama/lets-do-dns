"""letsencrypt's certbot Authentication Logic."""

from dns01_auth.command import run
from certbot_dns_auth.do_domain.record import Record


class Authenticate(object):
    """Handle letsencrypt DNS certificate identity authentication."""

    def __init__(self, environment, arguments=None):
        self._env = environment
        self._record = self._init_record()

    def perform(self):
        """Execute the authentication logic."""
        if self._in_post_hook_phase:
            self._delete_record()
            self._run_post_cmd()
        else:
            self._create_record()
            self._print_record_id()

        return 0

    @property
    def _in_post_hook_phase(self):
        return self._env.record_id is not None

    def _delete_record(self):
        self._record.number = self._env.record_id
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

        hostname = self._env.fqdn[0:domain_start]

        return hostname
