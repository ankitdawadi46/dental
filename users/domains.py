from abc import ABC, abstractmethod


# Interface to create a user
class IUserCreator(ABC):
    @abstractmethod
    def create_user(self, email: str, password: str):
        pass

# Interface to manage user group setup
class IGroupManager(ABC):
    @abstractmethod
    def add_user_to_group(self, user, group_name: str) -> None:
        pass

# Interface for site configuration
class ISiteConfigurator(ABC):
    @abstractmethod
    def configure_site(self, domain: str) -> None:
        pass
