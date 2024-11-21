import inject
from django.contrib.auth import get_user_model
from django_tenants.utils import tenant_context

from client.domains import ICreateClientUser
from client.models import Client
from users.domains import IGroupManager, ISiteConfigurator, IUserCreator

User = get_user_model()


class ClientUserCreator(ICreateClientUser):
    @inject.params(
        user_creator="UserCreator",
        group_manager="GroupManager",
        site_configurator="SiteConfigurator",
    )
    def __init__(
        self,
        user_creator: IUserCreator,
        group_manager: IGroupManager,
        site_configurator: ISiteConfigurator,
    ):
        self.user_creator = user_creator
        self.group_manager = group_manager
        self.site_configurator = site_configurator

    def create_user(self, client: Client, password: str) -> User:
        with tenant_context(client):
            # Create the user
            email = client.email
            user = self.user_creator.create_user(email, password)

            # Add user to SuperAdmin group
            self.group_manager.add_user_to_group(user, "SuperAdmin")

            # Configure the site
            self.site_configurator.configure_site(client.primary_domain_name)

        return user
