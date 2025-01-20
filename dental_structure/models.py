from django.db import models

from client.models import AuditFields

class Root(models.Model):
    name = models.CharField(max_length=255)
    d3_points = models.JSONField()  # Stores the D3 points as JSON

    def __str__(self):
        return self.name

class DentalStructure(models.Model):
    name = models.CharField(max_length=255)
    tooth_type = models.CharField(max_length=50)
    quadrant = models.CharField(max_length=50)
    num_roots = models.PositiveIntegerField()
    d3_points = models.JSONField()  # Stores the outline points as JSON
    roots = models.ManyToManyField(Root)

    def __str__(self):
        return self.name


class DentalTreatments(AuditFields):
    service_name = models.CharField(max_length=100)
    service_description = models.TextField()
    

class DentalTreatmentTypes(AuditFields):
    service_type_name = models.CharField(max_length=100)
    service_description = models.TextField()
    service_name = models.ForeignKey(
        DentalTreatments,
        on_delete=models.CASCADE,
        null=True, blank=True)
    

class DentalTreatmentProcedures(AuditFields):
    procedure_name = models.CharField(max_length=100)
    dental_service_type = models.ForeignKey(
        DentalTreatmentTypes, on_delete=models.CASCADE, null=True, blank=True
    )
    

class DentalDiagnosis(AuditFields):
    service_name = models.CharField(max_length=100)
    service_description = models.TextField()
    

class DentalDiagnosisTypes(AuditFields):
    service_type_name = models.CharField(max_length=100)
    service_description = models.TextField()
    service_name = models.ForeignKey(
        DentalDiagnosis,
        on_delete=models.CASCADE,
        null=True, blank=True)
    

class DentalDiagnosisProcedures(AuditFields):
    procedure_name = models.CharField(max_length=100)
    dental_service_type = models.ForeignKey(
        DentalDiagnosisTypes, on_delete=models.CASCADE, null=True, blank=True
    )