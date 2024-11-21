import CloudFlare
from django.conf import settings

from client.domains import ISetupDNS
from client.models import Client


class DNSSetup(ISetupDNS):
    def setup_dns(self, client: Client):
        token = getattr(settings, "DENTAL_APP_TOKEN", None)
        if token:
            cf = CloudFlare.CloudFlare(token=token)
            zone_id = getattr(settings, "ZONE_ID", "default-zone-id")
            pointing_ip = getattr(settings, "SERVER_IP_ADDRESS_POINT", "127.0.0.1")

            dns_record = {
                "name": client.primary_domain_name,
                "type": "A",
                "content": pointing_ip,
                "proxied": True,
            }
            cf.zones.dns_records.post(zone_id, data=dns_record)
