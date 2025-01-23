from client.selectors.client_profile_service import ClinicProfileService
from client.selectors.profile_service import ProfileService
from client.selectors.user_service import UserService


class UserCreationFactory:
    def __init__(self):
        self.user_service = UserService()
        self.profile_service = ProfileService()
        self.clinic_profile_service = ClinicProfileService()