from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings

from client.models import CustomUser
from users.domains import IForgotPasswordService
from users.selectors.factories.otp_email_factory import OTPEmailFactory
from utils.generate_otp import generate_otp


class ForgotPasswordService(IForgotPasswordService):
    """
    Concrete implementation of ForgotPasswordService.
    """

    def send_otp_email(self, email: str):
        """
        Send password reset email if the user exists.
        """
        try:
            # Get user by email
            user = CustomUser.objects.get(email=email)
            
            # Generate OTP for the forgot password process
            otp_value = generate_otp(user, purpose="ForgotPassword")

            # Send OTP email
            otp_email_factory = OTPEmailFactory()
            email_thread = otp_email_factory.create_email_thread_forget_password(user.email, otp_value)
            email_thread.start()

            return True
        except CustomUser.DoesNotExist:
            return False