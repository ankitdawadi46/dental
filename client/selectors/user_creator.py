from django.contrib.auth import get_user_model
from django_tenants.utils import tenant_context

from client.domains import ICreateClientUser
from client.models import Client
from users.selectors.group_manager import GroupManager
from users.selectors.site_configurator import SiteConfigurator
from users.selectors.user_creator import UserCreator

User = get_user_model()


class ClientUserCreator(ICreateClientUser):
    def __init__(
        self
    ):
        self.user_creator = UserCreator
        self.group_manager = GroupManager
        self.site_configurator = SiteConfigurator

    def create_user(self, client: Client, password: str) -> User:
            # Create the user
        email = client.email
        user = self.user_creator().create_user(email, password, is_staff=True)

            # Add user to SuperAdmin group
        self.group_manager().add_user_to_group(user, "SuperAdmin")

            # Configure the site
        self.site_configurator().configure_site(client.primary_domain_name)

        return user
