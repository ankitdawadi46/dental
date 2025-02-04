import secrets

from django.db import models
from django.utils.text import slugify

from client.models import AuditFields

# Create your models here.


class StockType(AuditFields):
    name = models.CharField(max_length=100, null=False, blank=False)


class Stock(AuditFields):
    # Basic stock details
    product_name = models.CharField(max_length=255)
    sku = models.CharField(
        max_length=100, unique=True
    )  # Stock Keeping Unit (unique identifier)
    description = models.TextField(blank=True, null=True)

    # Quantities and inventory tracking
    quantity_available = models.PositiveIntegerField(default=0)
    minimum_stock_level = models.PositiveIntegerField(
        default=0
    )  # For alerts when stock is low
    reorder_quantity = models.PositiveIntegerField(
        default=0
    )  # Recommended reorder amount

    # Pricing details
    cost_price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Cost price per unit
    selling_price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Selling price per unit
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.0
    )  # Optional discount %

    # Supplier and vendor details
    supplier_name = models.CharField(max_length=255, blank=True, null=True)
    supplier_contact = models.CharField(max_length=255, blank=True, null=True)

    # Location tracking
    warehouse_location = models.CharField(max_length=255, blank=True, null=True)
    aisle_number = models.CharField(max_length=50, blank=True, null=True)
    bin_number = models.CharField(max_length=50, blank=True, null=True)

    last_restocked_at = models.DateTimeField(blank=True, null=True)
    expiration_date = models.DateField(
        blank=True, null=True
    )  # Useful for perishable goods

    # Optional categorization
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.product_name} ({self.sku})"

    def is_low_stock(self):
        return self.quantity_available <= self.minimum_stock_level

    def calculate_margin(self):
        return self.selling_price - self.cost_price

    def save(self, *args, **kwargs):
        # Generate SKU if not provided
        if not self.sku:
            # Generate a slugified version of the product name and a random hash for uniqueness
            slugified_name = slugify(self.product_name)
            random_suffix = secrets.token_hex(
                4
            )  # Generates an 8-character random string
            self.sku = f"{slugified_name}-{random_suffix}".upper()
        super().save(*args, **kwargs)


class StockTransaction(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=10, choices=[("IN", "Stock In"), ("OUT", "Stock Out")]
    )
    quantity = models.PositiveIntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
