import random
from dental_app.utils.response import BaseResponse
from users.selectors.clinic_profile_creator import ClinicProfileCreator
from users.selectors.factories.otp_email_factory import OTPEmailFactory
from users.selectors.profile_creator import ProfileCreator
from users.selectors.user_creator import UserCreator
from utils.generate_otp import generate_otp


class SignUpFactory:
    def __init__(self, serializer):
        self.serializer = serializer

    def signup(self):
        try:
            # Create user using the UserService
            user_service = UserCreator()
            user = user_service.create_user(
                email=self.serializer.validated_data["email"],
                password=self.serializer.validated_data["password"],
                first_name=self.serializer.validated_data["first_name"],
                last_name=self.serializer.validated_data['last_name'],
            )
            # Use the correct tenant schema name
            # Create profile using the ProfileService
            profile_service = ProfileCreator()
            profile = profile_service.create_profile(
                user=user, profile_type=self.serializer.validated_data["profile_type"]
            )

            clinic_profile_creator = ClinicProfileCreator(
                clinic_name=self.serializer.validated_data["tenant_schema_name"],
                user=profile,
            )
            clinic_profile_creator.create_profile_client()
            otp_value = generate_otp(user, "SignUp")
            otp_email_factory = OTPEmailFactory()
            email_thread = otp_email_factory.create_email_thread_verification(user.email, otp_value)
            email_thread.start()
            return BaseResponse(
                data={"message": "OTP send to your email."},
                status=200,
            )
        except Exception as e:
            return BaseResponse(
                data={"error": f"An unexpected error occurred: {str(e)}"}, status=500
            )
