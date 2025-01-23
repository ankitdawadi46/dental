from client.domains import IProfileService
from client.serializers import ProfileSerializer


class ProfileService(IProfileService):
    def create_profile(self, profile_data):
        profile_serializer = ProfileSerializer(data=profile_data)
        if not profile_serializer.is_valid():
            raise ValueError(profile_serializer.errors)
        return profile_serializer.save()

    def update_profile(self, profile, profile_data):
        profile_serializer = ProfileSerializer(profile, data=profile_data, partial=True)
        if not profile_serializer.is_valid():
            raise ValueError(profile_serializer.errors)
        return profile_serializer.save()