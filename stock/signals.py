from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import StockTransaction

@receiver(post_save, sender=StockTransaction)
def handle_stock_transaction_save(sender, instance, created, **kwargs):
    stock = instance.stock
    transaction_type = instance.transaction_type
    quantity = instance.quantity

    if created:
        # New transaction - update stock
        pass
    else:
        # Updated transaction - recalculate stock based on changes
        old_instance = StockTransaction.objects.get(pk=instance.pk)
        old_quantity = old_instance.quantity
        old_transaction_type = old_instance.transaction_type

        # Revert old changes
        stock.quantity_available += old_quantity if old_transaction_type == "OUT" else -old_quantity

        # Apply new changes
        stock.quantity_available += quantity if transaction_type == "IN" else -quantity

    stock.save()

@receiver(post_delete, sender=StockTransaction)
def handle_stock_transaction_delete(sender, instance, **kwargs):
    stock = instance.stock
    transaction_type = instance.transaction_type
    quantity = instance.quantity

    # Revert stock adjustment
    stock.quantity_available += quantity if transaction_type == "OUT" else -quantity
    stock.save()