from rest_framework_simplejwt.tokens import RefreshToken
from users.domains import ITokenService


class JWTTokenService(ITokenService):
    def generate_tokens(self, user):
        """
        Generate JWT tokens for the given user.
        """
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }