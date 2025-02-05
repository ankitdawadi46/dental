from django.utils import timezone
import random
from client.models import OTP


def generate_otp(user, purpose="SignUp"):
    """
    Generates and stores the OTP along with the timestamp.
    """
    otp_value = random.randint(100000, 999999)  # Generate a 6-digit OTP
    otp_instance = OTP.objects.create(
        user=user,  # Link the OTP with the user
        otp=str(otp_value),
        created_at=timezone.now(),
        purpose=purpose
    )
    return otp_value