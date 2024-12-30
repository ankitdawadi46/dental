from dental_app.utils.response import BaseResponse
from users.selectors.clinic_profile_creator import ClinicProfileCreator
from users.selectors.profile_creator import ProfileCreator
from users.selectors.user_creator import UserCreator


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
            ) # Use the correct tenant schema name
                # Create profile using the ProfileService
            profile_service = ProfileCreator()
            profile = profile_service.create_profile(user=user)
            
            clinic_profile_creator = ClinicProfileCreator(
                clinic_name=self.serializer.validated_data["tenant_schema_name"],
                user=profile
                )
            clinic_profile_creator.create_profile_client()
            

            return BaseResponse(
                data={"message": "User created successfully."},
                status=201,
            )
        except Exception as e:
            return BaseResponse(
                data={"error": f"An unexpected error occurred: {str(e)}"}, status=500
            )
