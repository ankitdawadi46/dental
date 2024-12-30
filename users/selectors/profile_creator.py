from users.domains import IProfileCreatorService
from client.models import Profile

class ProfileCreator(IProfileCreatorService):
    def create_profile(self, user):
        """
        Creates a profile for the given user.
        """
        profile, _ = Profile.objects.get_or_create(user=user)
        return profile