from client.domains import IClinicProfileService
from client.models import ClinicProfile
from client.serializers import ClinicProfileSerializer


class ClinicProfileService(IClinicProfileService):
    def handle_clinic_profile(self, profile, clinic_data):
        clinic_profile = ClinicProfile.objects.filter(user=profile).first()
        clinic_data["user"] = profile.id

        if clinic_profile:
            clinic_serializer = ClinicProfileSerializer(
                clinic_profile, data=clinic_data, partial=True
            )
        else:
            clinic_serializer = ClinicProfileSerializer(data=clinic_data)

        if not clinic_serializer.is_valid():
            raise ValueError(clinic_serializer.errors)
        return clinic_serializer.save()