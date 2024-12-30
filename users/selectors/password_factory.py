from abc import ABC, abstractmethod

class PasswordFactory(ABC):
    """
    Abstract Factory Interface for creating password-related services.
    """

    @abstractmethod
    def create_forgot_password_service(self):
        pass

    @abstractmethod
    def create_reset_password_service(self):
        pass