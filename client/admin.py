from django.contrib import admin

from dental_app.utils.admin import admin_autoregister

from .models import *


class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "contact_number",
        "contact_person",
        "email",
        "is_enabled",
        "on_trial",
        "primary_domain_name",
    ]
    list_filter = ["is_enabled", "on_trial", "primary_domain_name"]
    search_fields = ["name", "contact_number", "contact_person"]
    # readonly_fields = ["created_on"]


class DomainAdmin(admin.ModelAdmin):
    list_display = ["domain", "tenant", "is_primary", "is_display_domain"]
    list_filter = [
        "domain",
        "tenant",
        "is_primary",
    ]  # list_display = ["name", "created_on"]
    # list_filter = ["is_primary", "is_enabled", "created_on"]
    # search_fields = ["name"]
    # readonly_fields = ["created_on"]


class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "client",
        "paid_fee",
        "next_payment_due_date",
        "transaction_id",
    ]
    list_filter = ["user", "client"]


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "client",
        "agreed_fee",
        "paid_fee",
        "enroll_date",
    ]
    list_filter = ["user", "client"]


admin.site.register(Client, ClientAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Payment, PaymentAdmin)

admin_autoregister("client", exclude_models=[Client])
