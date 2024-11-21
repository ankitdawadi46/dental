from django_tenants.utils import tenant_context
from django.utils.crypto import get_random_string

from client.domains import IClientSupportUserFactory
from client.models import Client
from users.selectors.group_manager import GroupManager
from users.selectors.user_creator import UserCreator


class ClientSupportUserFactory(IClientSupportUserFactory):
    def __init__(
        self,
        user_creator = UserCreator(),
        group_manager = GroupManager(),
    ):
        self.user_creator = user_creator
        self.group_manager = group_manager

    def create_support_user(self, client: Client):
        with tenant_context(client):
            hijacked_support_username = client.hijack_superuser_username
            password = get_random_string(20)
            user = self.user_creator.create_user(
                email=hijacked_support_username,
                first_name="DENTAL",
                last_name="SUPPORT",
                is_staff=True,
                is_superuser=True,
                password=password
            )
            self.group_manager.add_user_to_group(user, "SuperAdmin")
            return user, password
