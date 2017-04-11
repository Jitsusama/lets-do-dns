from digitalocean.domain import Record


class Authenticate(object):
    def __init__(self, environment):
        api_key = environment.get('DO_API_KEY')
        domain = environment.get('DO_DOMAIN')
        fqdn = environment.get('CERTBOT_DOMAIN')
        token = environment.get('CERTBOT_VALIDATION')

        hostname = fqdn[0:fqdn.rfind('.' + domain)]

        record = Record(api_key, domain, hostname)
        record.create(token)
