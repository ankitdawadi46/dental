from datetime import date

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from client.models import AuditFields, profile_directory_path, CustomUser

# class Client(TenantMixin):
#     name = models.CharField(max_length=100)
#     paid_until = models.DateField()
#     on_trial = models.BooleanField()
#     created_on = models.DateField(auto_now_add=True)

#     # default true, schema will be automatically created and synced when it is saved
#     auto_create_schema = True


# class Domain(DomainMixin):
#     pass



