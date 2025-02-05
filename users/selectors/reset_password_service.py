from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from client.models import OTP, CustomUser
from users.domains import IResetPasswordService


class ResetPasswordService(IResetPasswordService):
    """
    Concrete implementation of ResetPasswordService.
    """

    def reset_password(self, email: str, otp:OTP, new_password: str, confirm_password: str):
        """
        Reset password for the user if token is valid.
        """
        try:
            # Decode uid and get user
            user = CustomUser.objects.get(email=email)

            # Validate token
                # Check if passwords match
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return True
            else:
                return False
        except (CustomUser.DoesNotExist, ValueError):
            return False