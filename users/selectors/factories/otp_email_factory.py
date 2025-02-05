from users.domains import IEmailFactory
from users.selectors.otp_email_thread import OTPEmailVerificationThread, OTPEmailForgetPasswordThread


class OTPEmailFactory(IEmailFactory):
    def create_email_thread_verification(self, email, otp):
        """Create a thread to send the OTP email."""
        return OTPEmailVerificationThread(email, otp)
    
    def create_email_thread_forget_password(self, email, otp):
        """Create a thread to send the OTP email."""
        return OTPEmailForgetPasswordThread(email, otp)