from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection

User = get_user_model()


def user_with_profile_exists(email):
    try:
        # Attempt to fetch the user with the related profile in one query
        user = User.objects.select_related("user_profile").get(email=email)
        # If we reach this point, both the User and Profile exist
        user.refresh_from_db(fields=["user_profile"])
        if user.user_profile:
            return True
        else:
            return False
    except ObjectDoesNotExist:
        # If either the User or the Profile does not exist
        return False
