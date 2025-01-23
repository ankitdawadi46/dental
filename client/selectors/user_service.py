from client.domains import IUserService
from client.models import CustomUser
from client.serializers import CustomUserSerializer


class UserService(IUserService):
    def validate_profile_type(self, data):
        if data.get("profile_type") == "Doctor" and not data.get("nmc_no"):
            raise ValueError("NMC Number is required for Doctor")
        if data.get("profile_type") == "Helper" and not data.get("nhpc_no"):
            raise ValueError("NHPC Number is required for Helper")

    def get_or_create_user(self, user_data):
        user = CustomUser.objects.filter(email=user_data["email"]).first()
        if not user:
            user_serializer = CustomUserSerializer(data=user_data)
            if not user_serializer.is_valid():
                raise ValueError(user_serializer.errors)
            return user_serializer.save()
        return user
    
    def update_user(self, user, user_data):
        user_serializer = CustomUserSerializer(user, data=user_data, partial=True)
        if not user_serializer.is_valid():
            raise ValueError(user_serializer.errors)
        return user_serializer.save()