from typing import Dict

from django.utils.crypto import get_random_string

from client.domains import IClientCreationFactory
from client.models import Client
from client.selectors.client_creator import ClientCreator
from client.selectors.domain_setup import DomainSetup

# from client.selectors.dns_setup import DNSSetup
from client.selectors.user_creator import ClientUserCreator


class ClientCreationFactory(IClientCreationFactory):
    def __init__(self):
        self.client_creator = ClientCreator()
        self.domain_setup = DomainSetup()
        # self.dns_setup = DNSSetup()
        self.user_creator = ClientUserCreator()

    def create_client_with_dns_and_user(self, client_data: Dict) -> Client:
        # Step 1: Create the client
        client = self.client_creator.create_client(client_data)

        # Step 2: Setup Domain for the client
        self.domain_setup.setup_domain(client)

        # Step 3: Setup DNS for the client
        # self.dns_setup.setup_dns(client)

        # Step 4: Create user for the client
        password = get_random_string(10)
        self.user_creator.create_user(client, password)

        return client  # or return both client and user, as needed
