from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from client.models import ClinicProfile, CustomUser, Profile

User = get_user_model()


def user_with_profile_exists(email, profile_type, tenant_schema_name):
    try:
        # Attempt to fetch the user with the specified email
        user = CustomUser.objects.get(email=email)
        # Check if a profile with the specified profile_type exists for this 
        if Profile.objects.filter(user=user, profile_type=profile_type).exists():
            profile = Profile.objects.filter(user=user, profile_type=profile_type)[0]
    
        return (
            Profile.objects.filter(user=user, profile_type=profile_type).exists()
            and ClinicProfile.objects.select_related("clinic")
            .filter(clinic_id__schema_name=tenant_schema_name, user=profile)
            .exists()
        )
    except ObjectDoesNotExist:
        # If the user does not exist
        return False
