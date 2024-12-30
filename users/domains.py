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
    

class IAuthenticationService(ABC):
    @abstractmethod
    def authenticate_user(self, email, password):
        """
        Authenticates the user using email and password.
        """
        pass
    

class ITokenService(ABC):
    @abstractmethod
    def generate_tokens(self, user):
        """
        Generates JWT tokens for the given user.
        """
        pass
    

class IValidationService(ABC):
    @abstractmethod
    def validate_login_request(self, data):
        """
        Validates the login request data.
        """
        pass
    


class IProfileCreatorService(ABC):
    @abstractmethod
    def create_profile(self, user):
        """
        Validates the login request data.
        """
        pass
    

class IClinicProfileCreatorService(ABC):
    @abstractmethod
    def create_profile_client(self, user):
        """
        Validates the login request data.
        """
        pass
    

class IForgotPasswordService(ABC):
    """
    Interface for Forgot Password Service.
    """

    @abstractmethod
    def send_reset_email(self, email: str):
        pass
    

class IResetPasswordService(ABC):
    """
    Interface for Reset Password Service.
    """

    @abstractmethod
    def reset_password(self, uidb64: str, token: str, new_password: str, confirm_password: str):
        pass
