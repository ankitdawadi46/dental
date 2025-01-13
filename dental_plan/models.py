from django.db import models
from django.core.exceptions import ValidationError

from client.models import AuditFields, CustomUser
from dental_structure.models import DentalStructure
from stock.models import Stock


class Condition(AuditFields):
    name = models.CharField(max_length=255)
    condition_detail = models.TextField()


class Treatment(AuditFields):
    name = models.CharField(max_length=255)
    treatment_detail = models.TextField()


class PatientCondition(AuditFields):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    condition = models.ForeignKey(
        Condition, on_delete=models.CASCADE, null=True, blank=True, related_name="patient_conditions"
    )
    severity = models.CharField(
        max_length=100,
        choices=[("Mild", "Mild"), ("Moderate", "Moderate"), ("Severe", "Severe")],
    )
    d3_image = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class PatientTreatment(AuditFields):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    treatment = models.ForeignKey(
        Treatment, on_delete=models.CASCADE, null=True, blank=True,
        related_name="patient_treatments"
    )
    d3_image = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    

class TreatmentMaterialUsed(AuditFields):
    patient_treatment = models.ForeignKey(
        PatientTreatment, on_delete=models.CASCADE
    )
    material_used = models.ForeignKey(
        Stock, on_delete=models.CASCADE, blank=True, null=True
    )
    quantity = models.IntegerField(default=0, null=True, blank=True)
    
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
    
    

class Payment(AuditFields):
    patient_treatment = models.ForeignKey(
        PatientTreatment, on_delete=models.CASCADE, related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Failed", "Failed"),
        ],
        default="Pending",
    )
    notes = models.TextField(null=True, blank=True)
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )  # Discount amount
    discounted_amount = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False
    )  # Auto-calculated amount after discount
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False
    )
    
    def save(self, *args, **kwargs):
        # Ensure that discount amount does not exceed the total amount
        if self.discount_amount > self.amount:
            raise ValidationError("Discount amount cannot exceed the total amount.")

        # Calculate discounted amount and total amount
        self.discounted_amount = self.amount - self.discount_amount
        self.total_amount = self.amount  # Original amount (unchanged)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient_treatment.name} - {self.amount} - {self.payment_status}"


class DentalHistory(AuditFields):
    patient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="patient",
    )
    dental_structure = models.ForeignKey(
        DentalStructure, on_delete=models.CASCADE, related_name="dental_histories"
    )
    date = models.DateField()
    condition = models.ForeignKey(
        PatientCondition, on_delete=models.SET_NULL, null=True, blank=True
    )  # Link to the condition model
    treatment = models.ForeignKey(
        PatientTreatment, on_delete=models.SET_NULL, null=True, blank=True
    )  # Link to the treatment model
    notes = models.TextField(blank=True, null=True)
    doctor = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="doctor",
    )  # Any additional notes by the dentist

    def __str__(self):
        return f"{self.dental_structure.name} - {self.condition.name if self.condition else 'No Condition'} - {self.date}"
