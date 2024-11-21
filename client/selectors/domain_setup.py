from client.domains import ISetupDomain
from client.models import Client, Domain


class DomainSetup(ISetupDomain):
    def setup_domain(self, client: Client):
        domain = Domain()
        # TODO change the domain name after domain is verified. Use evironment file
        domain.domain = f"{client.primary_domain_name}.localhost"  # don't add your port or www here!
        domain.tenant = client
        domain.is_primary = True
        domain.save()
