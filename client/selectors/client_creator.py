from typing import Dict

from client.domains import ICreateClient
from client.models import Client


class ClientCreator(ICreateClient):
    def create_client(self, data: Dict) -> Client:
        # Remove ManyToManyField data from the main dictionary
        available_features = data.pop("available_features", None)
        # Create the Client object
        client = Client.objects.create(**data)

        # Handle ManyToManyField after creation
        if available_features:
            client.available_features.set(available_features)

        return client
