import datetime
from datetime import date

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from client.middleware import get_current_user


def profile_directory_path(instance, filename):
    time_stamp_str = f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}'
    return f"accounts/{get_current_user().id}/{'profile_' + time_stamp_str + '.jpg'}"


def get_current_user_adt():
    try:
        return get_current_user()
    except Exception:
        return None


# class Client(TenantMixin):
#     name = models.CharField(max_length=100)
#     paid_until = models.DateField()
#     on_trial = models.BooleanField()
#     created_on = models.DateField(auto_now_add=True)

#     # default true, schema will be automatically created and synced when it is saved
#     auto_create_schema = True


# class Domain(DomainMixin):
#     pass


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class AuditFields(models.Model):
    created_by = models.ForeignKey(
        User,
        related_name="%(class)s_createdby",
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        default=get_current_user_adt(),
    )
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified_date = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeletionManager()

    class Meta:
        abstract = True

    def delete(self, hard=False):
        if not hard:
            self.deleted_at = timezone.now()
            super().save()
        else:
            super().delete()


class Profile(AuditFields):
    profile_type = (
        ("Doctor", "Doctor"),
        ("Intern", "Intern"),
        ("Helper", "Helper"),
        ("Client", "Client")
    )
    gender = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="user_profile",
    )
    photo = models.FileField(
        upload_to=profile_directory_path,
        validators=[
            FileExtensionValidator(allowed_extensions=settings.VALID_IMAGE_FORMAT)
        ],
        null=True,
    )
    dob = models.DateField(("Date of Birth"), null=True, blank=True)
    gender = models.CharField(
        ("Gender"), choices=gender, max_length=50, null=True, blank=True
    )
    profile_type = models.CharField(
        ("Profile Type"), choices=profile_type, max_length=30, null=True, blank=True
    )
    designation = models.CharField(
        ("Designation"), max_length=50, null=True, blank=True
    )
    address = models.CharField(("Address"), max_length=50, null=True, blank=True)
    phone_number = models.CharField(
        ("Phone Number"), max_length=15, null=True, blank=True
    )
    nmc_no = models.CharField(
        ("NMC No"), max_length=30, null=True, blank=True)
    nhpc_no = models.CharField(
        ("NHPC No"), max_length=30, blank=True, null=True
    )

    class Meta:
        verbose_name_plural = "Profile"

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_age(self):
        if self.dob:
            today = date.today()
            age = (
                today.year
                - self.dob.year
                - ((today.month, today.day) < (self.dob.month, self.dob.day))
            )
            return str(age) + " " + " "
        else:
            return None

    def get_avatar(self):
        url = "https://ui-avatars.com/api/?background=0D8ABC&color=fff&name={0}+{1}&size=256&format=png".format(
            self.user.first_name, self.user.last_name
        )
        return url

    def get_photo(self):
        try:
            a = self.photo
            return a.url
        except Exception:
            return self.get_avatar()
