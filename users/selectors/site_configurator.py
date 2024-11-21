from django.contrib.sites.models import Site

from users.domains import ISiteConfigurator


class SiteConfigurator(ISiteConfigurator):
    def configure_site(self, domain: str) -> None:
        site, _ = Site.objects.get_or_create(id=1)
        site.domain = domain
        site.name = domain
        site.save()
