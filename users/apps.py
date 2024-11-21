import inject
from django.apps import AppConfig


# Configure the inject container
def configure_injections(binder):
    from users.selectors.group_manager import GroupManager
    from users.selectors.site_configurator import SiteConfigurator
    from users.selectors.user_creator import UserCreator

    binder.bind("UserCreator", UserCreator())
    binder.bind("GroupManager", GroupManager())
    binder.bind("SiteConfigurator", SiteConfigurator())


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        inject.configure_once(configure_injections)
