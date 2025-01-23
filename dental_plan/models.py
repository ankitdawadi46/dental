from django.core.exceptions import ValidationError
from django.db import models

from client.models import AuditFields, CustomUser
from dental_structure.models import (
    DentalDiagnosisProcedures,
    DentalDiagnosisTypes,
    DentalStructure,
    DentalTreatmentProcedures,
    DentalTreatmentTypes,
)
from stock.models import Stock


# class PatientCondition(AuditFields):
#     name = models.CharField(max_length=255)
#     description = models.TextField(null=True, blank=True)
#     condition = models.ForeignKey(
#         Condition,
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name="patient_conditions",
#     )
#     severity = models.CharField(
#         max_length=100,
#         choices=[("Mild", "Mild"), ("Moderate", "Moderate"), ("Severe", "Severe")],
#     )
#     d3_image = models.JSONField(null=True, blank=True)

#     def __str__(self):
#         return self.name

class CompanyDiagnosticProcedures(AuditFields):
    service_type_id = models.ForeignKey(
        DentalDiagnosisTypes, on_delete=models.CASCADE, null=True, blank=True
    )
    procedure_id = models.ForeignKey(
        DentalDiagnosisProcedures, on_delete=models.CASCADE, null=True, blank=True
    )
    procedure_name = models.CharField(null=True, blank=True, max_length=255)
    service_type_name = models.CharField(null=True, blank=True, max_length=255)


class CompanyTreatmentProcedures(AuditFields):
    service_type_id = models.ForeignKey(
        DentalTreatmentTypes, on_delete=models.CASCADE, null=True, blank=True
    )
    procedure_id = models.ForeignKey(
        DentalTreatmentProcedures, on_delete=models.CASCADE, null=True, blank=True
    )
    procedure_name = models.CharField(null=True, blank=True, max_length=255)
    service_type_name = models.CharField(null=True, blank=True, max_length=255)
    price = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)


class CompanyTreamentProcedureSession(AuditFields):
    company_treatment_procedures = models.ForeignKey(
        CompanyTreatmentProcedures,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="company_treatment_procedure_sessions",
    )
    session_name = models.CharField(null=True, blank=True, max_length=255)
    session_duration_hour = models.IntegerField(null=True, blank=True)
    session_duration_min = models.IntegerField(null=True, blank=True)


class TreatmentMaterialUsed(AuditFields):
    patient_treatment = models.ForeignKey(
        CompanyTreatmentProcedures,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="treatment_material_used",
    )
    material_used = models.ForeignKey(
        Stock, on_delete=models.CASCADE, blank=True, null=True
    )
    quantity = models.IntegerField(default=0, null=True, blank=True)
    
    
class PatientDentalDiagnostics(AuditFields):
    patient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="dental_diagnostic_plan_custom_user"
    )
    dental_structure = models.ForeignKey(
        DentalStructure,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="dental_diagnostic_plan_dental_structure",
    )
    dental_diagnostics = models.ForeignKey(
        CompanyDiagnosticProcedures, on_delete=models.CASCADE, blank=True, null=True, 
        related_name="dental_diagnostic_plan_dental_diagnostics"
    )
    


class PatientDentalTreatmentPlans(AuditFields):
    patient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="dental_treatment_plan_custom_user"
    )
    dental_structure = models.ForeignKey(
        DentalStructure,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="dental_treatment_plan_dental_structure",
    )
    dental_procedures = models.ForeignKey(
        CompanyTreatmentProcedures,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="dental_treatment_patient_plan_dental_procedures",
    )
    is_existing = models.BooleanField(null=True, blank=True)
    is_planned = models.BooleanField(null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     # Check if the object is being created or updated
    #     if not self.pk:  # This is for creation
    #         # Update stock when the object is created
    #         if self.material_used:
    #             self.material_used.quantity_available -= self.quantity
    #             self.material_used.save()

    #     else:
    #         old_instance = TreatmentMaterialUsed.objects.get(id=self.pk)
    #         old_instance.material_used.quantity_available += old_instance.quantity
    #         old_instance.save()
    #         if self.material_used:
    #             self.material_used.quantity_available -= self.quantity
    #             self.material_used.save()
    #     super(TreatmentMaterialUsed, self).save(*args, **kwargs)

    # class Payment(AuditFields):
    # patient_treatment = models.ForeignKey(
    #     CompanyTreatmentProcedures, on_delete=models.CASCADE, related_name="payments"
    # )
    # amount = models.DecimalField(max_digits=10, decimal_places=2)
    # payment_date = models.DateField()
    # payment_method = models.CharField(max_length=50, null=True, blank=True)
    # payment_status = models.CharField(
    #     max_length=20,
    #     choices=[
    #         ("Pending", "Pending"),
    #         ("Completed", "Completed"),
    #         ("Failed", "Failed"),
    #     ],
    #     default="Pending",
    # )
    # notes = models.TextField(null=True, blank=True)
    # discount_amount = models.DecimalField(
    #     max_digits=10, decimal_places=2, default=0.00
    # )  # Discount amount
    # discounted_amount = models.DecimalField(
    #     max_digits=10, decimal_places=2, editable=False
    # )  # Auto-calculated amount after discount
    # total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    # def save(self, *args, **kwargs):
    #     # Ensure that discount amount does not exceed the total amount
    #     if self.discount_amount > self.amount:
    #         raise ValidationError("Discount amount cannot exceed the total amount.")

    #     # Calculate discounted amount and total amount
    #     self.discounted_amount = self.amount - self.discount_amount
    #     self.total_amount = self.amount  # Original amount (unchanged)
    #     super().save(*args, **kwargs)

    # def __str__(self):
    #     return f"{self.patient_treatment.name} - {self.amount} - {self.payment_status}"


# class DentalHistory(AuditFields):
#     patient = models.ForeignKey(
#         CustomUser,
#         on_delete=models.CASCADE,
#         null=False,
#         blank=False,
#         related_name="patient",
#     )
#     dental_structure = models.ForeignKey(
#         DentalStructure, on_delete=models.CASCADE, related_name="dental_histories"
#     )
#     date = models.DateField()
#     condition = models.ForeignKey(
#         PatientCondition, on_delete=models.SET_NULL, null=True, blank=True
#     )  # Link to the condition model
#     treatment = models.ForeignKey(
#         PatientTreatment, on_delete=models.SET_NULL, null=True, blank=True
#     )  # Link to the treatment model
#     notes = models.TextField(blank=True, null=True)
#     doctor = models.ForeignKey(
#         CustomUser,
#         null=True,
#         blank=True,
#         on_delete=models.CASCADE,
#         related_name="doctor",
#     )  # Any additional notes by the dentist

#     def __str__(self):
#         return f"{self.dental_structure.name} - {self.condition.name if self.condition else 'No Condition'} - {self.date}"
