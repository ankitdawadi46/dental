from django_tenants.utils import schema_context

from client.domains import ISetupDomain
from client.models import Client, Domain


class DomainSetup(ISetupDomain):
    def setup_domain(self, client: Client):
        with schema_context('public'):
            domain = Domain()
            # TODO change the domain name after domain is verified. Use evironment file
            domain.domain = f"{client.primary_domain_name}.pythonapi.nimtoz.com"  # don't add your port or www here!
            domain.tenant = client
            domain.is_primary = True
            domain.save()
