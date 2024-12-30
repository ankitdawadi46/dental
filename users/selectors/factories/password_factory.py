from users.selectors.forget_password_service import ForgotPasswordService
from users.selectors.password_factory import PasswordFactory
from users.selectors.reset_password_service import ResetPasswordService


class DefaultPasswordFactory(PasswordFactory):
    """
    Concrete Factory for creating the default forgot password and reset password services.
    """

    def create_forgot_password_service(self):
        return ForgotPasswordService()

    def create_reset_password_service(self):
        return ResetPasswordService()