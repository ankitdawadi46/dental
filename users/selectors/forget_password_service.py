from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings

from client.models import CustomUser
from users.domains import IForgotPasswordService


class ForgotPasswordService(IForgotPasswordService):
    """
    Concrete implementation of ForgotPasswordService.
    """

    def send_reset_email(self, email: str):
        """
        Send password reset email if the user exists.
        """
        try:
            # Get user by email
            user = CustomUser.objects.get(email=email)
            
            # Generate token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())

            # Generate reset URL
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            import ipdb; ipdb.set_trace()

            # Send reset password email
            subject = 'Password Reset Request'
            message = f'Click the link to reset your password: {reset_url}'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

            return True
        except CustomUser.DoesNotExist:
            return False