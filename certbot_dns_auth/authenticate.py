"""letsencrypt's certbot Authentication Logic."""

from do_record import Record
from certbot_dns_auth.printer import printer


class Authenticate(object):
    """Handle letsencrypt DNS certificate identity authentication."""

    def __init__(self, environment):
        self.api_key = environment.get('DO_API_KEY')
        self.domain = environment.get('DO_DOMAIN')
        self.fqdn = environment.get('CERTBOT_DOMAIN')
        self.validation_key = environment.get('CERTBOT_VALIDATION')
        self.record_id = environment.get('CERTBOT_AUTH_OUTPUT')

    def perform(self):
        """Execute the authentication logic."""
        if self._in_post_hook_phase:
            self._delete_record()
        else:
            record_id = self._create_record()
            printer(record_id)

        return 0

    @property
    def _in_post_hook_phase(self):
        return self.record_id is not None

    def _delete_record(self):
        record = self._init_record()
        record.delete(self.record_id)

    def _create_record(self):
        record = self._init_record()
        return record.create(self.validation_key)

    def _init_record(self):
        hostname = self._parse_hostname()
        record = Record(self.api_key, self.domain, hostname)
        return record

    def _parse_hostname(self):
        domain_start_index = self.fqdn.rfind('.' + self.domain)
        fqdn_start_index = 0

        hostname = self.fqdn[fqdn_start_index:domain_start_index]

        return hostname
