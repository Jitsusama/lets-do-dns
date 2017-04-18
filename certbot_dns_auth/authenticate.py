"""letsencrypt's certbot Authentication Logic."""

from do_record import Record
from certbot_dns_auth.command import run


class Authenticate(object):
    """Handle letsencrypt DNS certificate identity authentication."""

    def __init__(self, environment):
        # Set internal state according to environment variable inputs.
        self.api_key = environment.get('DO_API_KEY')
        self.domain = environment.get('DO_DOMAIN')
        self.fqdn = environment.get('CERTBOT_DOMAIN')
        self.validation_key = environment.get('CERTBOT_VALIDATION')
        self.record_id = environment.get('CERTBOT_AUTH_OUTPUT')
        self.post_cmd = environment.get('LETS_DO_POSTCMD')

        # Using inputs, create a DNS record object.
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
        return self.record_id is not None

    def _delete_record(self):
        self._record.number = self.record_id
        self._record.delete()

    def _run_post_cmd(self):
        if self.post_cmd:
            run(self.post_cmd)

    def _create_record(self):
        self._record.create(self.validation_key)

    def _print_record_id(self):
        self._record.printer()

    def _init_record(self):
        hostname = self._parse_hostname()
        record = Record(self.api_key, self.domain, hostname)
        return record

    def _parse_hostname(self):
        domain_suffix = '.' + self.domain
        domain_start = self.fqdn.rfind(domain_suffix)

        hostname = self.fqdn[0:domain_start]

        return hostname
