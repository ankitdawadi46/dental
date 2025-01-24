from client.models import ClinicProfile
from dental_app.utils.exceptions import AuthenticationError
from users.selectors.authentication_service import AuthenticationService
from users.selectors.token_service import JWTTokenService
from users.selectors.validation_service import ValidationService


class LoginFactory:
    def __init__(self, request):
        # Using Dependency Injection to inject concrete implementations
        self.authentication_service_factory = AuthenticationService()
        self.token_service_factory = JWTTokenService()
        self.validation_service_factory = ValidationService()
        self.data = request.data

    def login(self):
        # Validate request data
        email, password, remember_me = (
            self.validation_service_factory.validate_login_request(self.data)
        )

        # Authenticate the user
        user = self.authentication_service_factory.authenticate_user(email, password)
        if not user:
            raise AuthenticationError(
                message={"error": "Invalid email and/or password"}, code=401
            )
        # Generate tokens for the authenticated user
        tokens = self.token_service_factory.generate_tokens(user)
        if not user.is_superuser:
            clinic_profiles = ClinicProfile.objects.select_related(
                "clinic",
                "user" 
                ).filter(user__user__email=user.email)
            tokens['client_schema_name'] = [{
                'schema_name': clinic_profile.clinic.schema_name,
                'clinic_id': clinic_profile.clinic.id} for clinic_profile in clinic_profiles]
        return tokens
