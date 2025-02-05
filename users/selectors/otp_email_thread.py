import threading
from django.core.mail import send_mail
from django.conf import settings

class OTPEmailVerificationThread(threading.Thread):
    def __init__(self, email, otp):
        super().__init__()
        self.email = email
        self.otp = otp

    def run(self):
        """Override the run method to send the email."""
        try:
            send_mail(
                "Your OTP Code",
                f"Your verification code is: {self.otp}",
                settings.DEFAULT_FROM_EMAIL,
                [self.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send OTP to {self.email}: {str(e)}")
            

class OTPEmailForgetPasswordThread(threading.Thread):
    def __init__(self, email, otp):
        super().__init__()
        self.email = email
        self.otp = otp

    def run(self):
        """Override the run method to send the email."""
        try:
            send_mail(
                "Your OTP Code",
                f"Your verification code is: {self.otp}",
                settings.DEFAULT_FROM_EMAIL,
                [self.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send OTP to {self.email}: {str(e)}")