from do_record import Record
from printer import printer


class Authenticate(object):
    """Handle letsencrypt DNS certificate identity authentication."""

    def __init__(self, environment):
        self.api_key = environment.get('DO_API_KEY')
        self.domain = environment.get('DO_DOMAIN')
        self.fqdn = environment.get('CERTBOT_DOMAIN')
        self.validation_key = environment.get('CERTBOT_VALIDATION')

    def perform(self):
        try:
            self._create_record()
        finally:
            return 0

    def _create_record(self):
        hostname = self._parse_hostname()

        record = Record(self.api_key, self.domain, hostname)
        record_id = record.create(self.validation_key)
        printer(record_id)

    def _parse_hostname(self):
        domain_start_index = self.fqdn.rfind('.' + self.domain)
        fqdn_start_index = 0

        hostname = self.fqdn[fqdn_start_index:domain_start_index]

        return hostname
