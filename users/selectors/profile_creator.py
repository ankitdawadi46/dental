from users.domains import IProfileCreatorService
from client.models import Profile

class ProfileCreator(IProfileCreatorService):
    def create_profile(self, user, profile_type):
        """
        Creates a profile for the given user.
        """
        profile, created = Profile.objects.get_or_create(user=user, profile_type=profile_type)
        return profile
            
        