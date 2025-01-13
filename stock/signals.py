import requests
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from dental_plan.models import TreatmentMaterialUsed
from stock.models import Stock

@receiver(post_delete, sender=TreatmentMaterialUsed)
def delete_tretment_material_used(sender, instance, **kwargs):
    stock = Stock.objects.get(id=instance.material_used.id)
    stock.quantity_available += instance.quantity
    stock.save()

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
    
    
@receiver(pre_save, sender=TreatmentMaterialUsed)
def update_stock_on_pre_save(sender, instance, **kwargs):
    # Check if the object is being updated (exists in the database)
    if instance.pk:
        # Fetch the existing instance before updates
        old_instance = TreatmentMaterialUsed.objects.get(pk=instance.pk)

        # Handle case when `material_used` is updated
        if old_instance.material_used != instance.material_used:
            # Revert stock for the old material
            if old_instance.material_used:
                old_instance.material_used.quantity_available += old_instance.quantity
                old_instance.material_used.save()

            # Deduct stock for the new material
            if instance.material_used:
                instance.material_used.quantity_available -= instance.quantity
                instance.material_used.save()

        # Handle case when only `quantity_used` is updated
        elif old_instance.quantity != instance.quantity:
            # Adjust stock for the same material
            if instance.material_used:
                # Revert the old quantity
                instance.material_used.quantity_available += old_instance.quantity

                # Deduct the new quantity
                instance.material_used.quantity_available -= instance.quantity
                instance.material_used.save()

    else:  # This is for creation
        if instance.material_used:
            if instance.material_used.quantity_available >= instance.quantity:
            # Deduct stock for the material used
                instance.material_used.quantity_available -= instance.quantity
                instance.material_used.save()
            else:
                raise ValueError("insufficient stock data")
                # send_error_to_api(str(e), "pre_save", instance)
