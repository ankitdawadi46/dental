from django.contrib.auth import authenticate
from users.domains import IAuthenticationService


class AuthenticationService(IAuthenticationService):
    def authenticate_user(self, email, password):
        """
        Authenticates the user using email and password.
        """
        return authenticate(email=email, password=password)