from users.domains import IClinicProfileCreatorService
from client.models import Client, ClinicProfile

class ClinicProfileCreator(IClinicProfileCreatorService):
    
    def __init__(self, clinic_name, user):
        self.clinic_name = clinic_name
        self.user = user
        
    def get_clinic_from_name(self):
        clinic = Client.objects.get(schema_name=self.clinic_name)
        if not clinic:
            raise ValueError("User most be related to atleast one client")
        return clinic
        
    def create_profile_client(self):
        """
        Creates a profile for the given user.
        """
        profile = ClinicProfile.objects.create(
            clinic=self.get_clinic_from_name(),
            user=self.user)
        return profile