"""letsencrypt's certbot authentication logic."""

from lets_do_dns.acme_dns_auth.command import run
from lets_do_dns.acme_dns_auth.time_delay import sleep
from lets_do_dns.dns_tools.lookup import lookup
from lets_do_dns.do_domain.resource import Resource
from lets_do_dns.printer import stdout


class Authenticate(object):
    """Handle letsencrypt DNS certificate identity authentication."""

    def __init__(self, environment):
        self._env = environment
        self._resource = self._init_resource()

    def perform(self):
        """Execute the authentication logic."""
        if self._in_authentication_hook_stage:
            self._create_resource()
            self._print_record_id()
            self._delay_finish()
            self._verify_resource_exists()

        if self._in_cleanup_hook_stage:
            self._delete_resource()
            self._run_post_cmd()

    @property
    def _in_authentication_hook_stage(self):
        return self._env.record_id is None

    @property
    def _in_cleanup_hook_stage(self):
        return self._env.record_id is not None

    def _delete_resource(self):
        self._resource.delete()

    def _run_post_cmd(self):
        if self._env.post_cmd:
            run(self._env.post_cmd,
                env={'CERTBOT_HOSTNAME': self._env.fqdn})

    def _create_resource(self):
        self._resource.create()

    def _verify_resource_exists(self):
        fqdn = '{}.{}'.format(self._parse_hostname(), self._env.domain)

        return lookup(fqdn)

    def _print_record_id(self):
        stdout(self._resource.__int__())

    def _init_resource(self):
        hostname = self._parse_hostname()
        record = Resource(
            self._env.api_key, hostname, self._env.domain,
            self._env.validation_key, self._env.record_id)
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
