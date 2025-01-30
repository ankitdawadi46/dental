import requests
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from dental_plan.models import PatientDentalTreatmentPlans, TreatmentMaterialUsed
from stock.models import Stock

@receiver(post_delete, sender=PatientDentalTreatmentPlans)
def restore_stock_on_treatment_plan_delete(sender, instance, **kwargs):
    """
    Restores stock when a PatientDentalTreatmentPlans instance is deleted.
    """
    # Fetch related treatment materials
    treatment_materials = TreatmentMaterialUsed.objects.filter(
        patient_treatment=instance.dental_procedures
    ).select_related("material_used")

    for material in treatment_materials:
        if material.material_used:
            material.material_used.quantity_available += material.quantity
            material.material_used.save()

API_ENDPOINT = "http://localhost:8888/error-api/"

def send_error_to_api(error_message, signal_type, instance):
    """
    Send error details to an external API.
    """
    data = {
        "error_message": error_message,
        "signal_type": signal_type,
        "model": instance.__class__.__name__,
        "instance_id": instance.pk,
    }
    try:
        response = requests.post(API_ENDPOINT, json=data, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    except requests.RequestException as e:
        pass
    
@receiver(pre_save, sender=PatientDentalTreatmentPlans)   
def update_stock_on_pre_save(sender, instance, **kwargs):
    """
    Adjusts stock when a PatientDentalTreatmentPlans instance is updated.
    """
    if instance.pk:
        # Fetch the existing PatientDentalTreatmentPlans object before update
        old_instance = PatientDentalTreatmentPlans.objects.get(pk=instance.pk)

        # Fetch related treatment materials
        treatment_materials = TreatmentMaterialUsed.objects.filter(
            patient_treatment=old_instance.dental_procedures
        ).select_related("material_used")

        for old_instance_material in treatment_materials:
            if old_instance_material.material_used:
                # Restore stock for the old instance before the update
                old_instance_material.material_used.quantity_available += old_instance_material.quantity
                old_instance_material.material_used.save()

                # Handle quantity update (deduct stock after update)
                new_quantity = 0  # Define your new quantity logic based on the update
                if old_instance_material.quantity != new_quantity:
                    if old_instance_material.material_used.quantity_available >= new_quantity:
                        old_instance_material.material_used.quantity_available -= new_quantity
                        old_instance_material.material_used.save()
                    else:
                        raise ValueError("Insufficient stock for material")

    else:
        # Handle the creation scenario (similar logic for stock adjustment)
        treatment_materials = TreatmentMaterialUsed.objects.filter(
            patient_treatment=instance.dental_procedures
        ).select_related("material_used")

        for material in treatment_materials:
            if material.material_used:
                if material.material_used.quantity_available >= material.quantity:
                    material.material_used.quantity_available -= material.quantity
                    material.material_used.save()
                else:
                    raise ValueError(f"Insufficient stock for material: {material.material_used}")
