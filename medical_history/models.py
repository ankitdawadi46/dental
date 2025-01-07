from django.db import models

from client.models import AuditFields, CustomUser


# Create your models here9.
class MedicalHistoryTypes(AuditFields):
    type_name = models.CharField(max_length=100, null=True, blank=True)


class MedicalHistory(AuditFields):
    patient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="medical_patient",
    )
    medical_history_type = models.ForeignKey(
        MedicalHistoryTypes, on_delete=models.CASCADE, null=True
    )
    description = models.TextField(null=True, blank=True)
    medicine_history = models.TextField(null=True, blank=True)
    allergy_history = models.TextField(null=True, blank=True)
    diagnosis_date = models.DateField(null=True, blank=True)
