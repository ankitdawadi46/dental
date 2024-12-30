
from users.domains import IValidationService

class ValidationService(IValidationService):
    def validate_login_request(self, data):
        """
        Validates the login request payload.
        """
        email = data.get("email")
        password = data.get("password")
        remember_me = data.get("remember_me", False)

        if not email or not password:
            raise ValueError("Email and password are required.")

        return email, password, remember_me