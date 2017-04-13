from do_record.record import Record
from printer import Printer


class Authenticate(object):
    """Handle letsencrypt DNS certificate identity authentication."""

    def __init__(self, environment):
        self.api_key = environment.get('DO_API_KEY')
        self.domain = environment.get('DO_DOMAIN')
        self.fqdn = environment.get('CERTBOT_DOMAIN')
        self.validation_key = environment.get('CERTBOT_VALIDATION')

        self._create_record()

    def _create_record(self):
        hostname = self._parse_hostname()

        record = Record(self.api_key, self.domain, hostname)
        record_id = record.create(self.validation_key)
        Printer(record_id)

    def _parse_hostname(self):
        domain_start_index = self.fqdn.rfind('.' + self.domain)
        fqdn_start_index = 0

        hostname = self.fqdn[fqdn_start_index:domain_start_index]

        return hostname
