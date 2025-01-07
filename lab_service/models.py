from django.db import models

from client.models import AuditFields, CustomUser

# Create your models here.
class LabService(AuditFields):
    service_name = models.CharField(null=False, blank=False, max_length=100, default="Xray")
    service_description = models.TextField(null=True, blank=True)
    quantity = models.DecimalField(null=True, blank=True)
    doctor = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)