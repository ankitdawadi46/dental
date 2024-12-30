from django.db import models

from dental_structure.models import DentalStructure
from client.models import AuditFields, CustomUser


class Condition(AuditFields):
    name = models.CharField(max_length=255)
    condition_detail = models.TextField()
    

class Treatment(AuditFields):
    name = models.CharField(max_length=255)
    treatment_detail = models.TextField()


class PatientCondition(AuditFields):
    name = models.CharField(max_length=255)
    description = models.TextField()
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, null=False, blank=False)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, null=False, blank=False)
    severity = models.CharField(max_length=100, choices=[('Mild', 'Mild'), ('Moderate', 'Moderate'), ('Severe', 'Severe')])
    d3_image = models.JSONField()

    def __str__(self):
        return self.name


class PatientTreatment(AuditFields):
    name = models.CharField(max_length=255)
    description = models.TextField()
    material_used = models.CharField(max_length=255, blank=True, null=True)
    d3_image = models.JSONField()

    def __str__(self):
        return self.name
    

class DentalHistory(AuditFields):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    dental_structure = models.ForeignKey(DentalStructure, on_delete=models.CASCADE, related_name='dental_histories')
    date = models.DateField()
    condition = models.ForeignKey(Condition, on_delete=models.SET_NULL, null=True, blank=True)  # Link to the condition model
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True, blank=True)  # Link to the treatment model
    notes = models.TextField(blank=True, null=True)  # Any additional notes by the dentist

    def __str__(self):
        return f"{self.dental_structure.name} - {self.condition.name if self.condition else 'No Condition'} - {self.date}"
