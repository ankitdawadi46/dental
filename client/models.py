import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone
from django.utils.timesince import timesince
from django_tenants.models import DomainMixin, TenantMixin
from django_tenants_celery_beat.models import PeriodicTaskTenantLinkMixin


class PeriodicTaskTenantLink(PeriodicTaskTenantLinkMixin):
    pass


class DateTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class SoftwareFeatures(DateTimeModel):
    name = models.CharField(max_length=255)
    identifier_slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Software Features"
        verbose_name = "Software Feature"

    def __str__(self):
        return self.name


class Client(TenantMixin):
    name = models.CharField(max_length=1024, verbose_name="business name")
    paid_until = models.DateTimeField(null=True, blank=True)
    contact_number = models.CharField(null=True, blank=True, max_length=20)
    contact_person = models.CharField(null=True, blank=True, max_length=255)
    email = models.EmailField(null=True, blank=True)
    is_enabled = models.BooleanField(default=True)
    on_trial = models.BooleanField(default=False)
    primary_domain_name = models.CharField(null=True, blank=True, max_length=512)
    created_on = models.DateField(auto_now_add=True)
    available_features = models.ManyToManyField(SoftwareFeatures, null=True, blank=True)
    auto_create_schema = True

    def get_client_url(self):
        return "https://{}".format(self.primary_domain_name)

    @property
    def time_since_due_passed(self):
        if self.paid_until:
            # Ensure both times are timezone-aware and convert to a string
            if timezone.is_aware(self.paid_until):
                return timesince(self.paid_until, timezone.now())
            else:
                # Handle naive datetime objects (if applicable)
                return timesince(
                    self.paid_until,
                    timezone.now().astimezone(timezone.get_current_timezone()),
                )
        return None

    @property
    def hijack_superuser_username(self):
        try:
            username = settings.TENANT_HIJACK_SUPERUSER_USERNAME
        except AttributeError:
            username = "super"
        hijack_username = f"{username}@{self.primary_domain_name}"
        return hijack_username


class Domain(DomainMixin):
    ns_records = models.JSONField(null=True, blank=True)
    zone_id = models.CharField(max_length=512, null=True, blank=True)
    is_display_domain = models.BooleanField(default=False)

    def has_cf_configured(self):
        if self.zone_id:
            return True
        else:
            return False


class PaymentManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("client")


class Payment(DateTimeModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    client = models.OneToOneField(Client, on_delete=models.DO_NOTHING)
    agreed_fee = models.BigIntegerField()
    paid_fee = models.BigIntegerField()
    enroll_date = models.DateField()
    payment_due_date = models.DateField()
    active_status = models.BooleanField(default=False)
    additional_note = models.TextField(blank=True, null=True)
    additional_contact_no = models.BigIntegerField(blank=True, null=True)
    campaign_id = models.IntegerField(blank=True, null=True)

    objects = PaymentManger()

    def __str__(self):
        return (
            f"client: {self.client} - agreed: {self.agreed_fee} - paid: {self.paid_fee}"
        )

    def get_due_blance(self):
        return int(self.agreed_fee) - int(self.paid_fee)


class Invoice(DateTimeModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    paid_fee = models.BigIntegerField()
    next_payment_due_date = models.DateField()
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.client} - {self.next_payment_due_date}"

    class Meta:
        ordering = ("next_payment_due_date",)


from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=Invoice)
def adjust_paid_fee_on_update(sender, instance, **kwargs):
    if instance.pk:  # If the instance is being updated
        old_invoice = Invoice.objects.get(pk=instance.pk)
        fee_difference = instance.paid_fee - old_invoice.paid_fee
        if fee_difference != 0:
            client_payment = Payment.objects.get(
                user=instance.user, client=instance.client
            )
            client_payment.paid_fee += fee_difference
            client_payment.payment_due_date = instance.next_payment_due_date
            client_payment.save()


@receiver(post_save, sender=Invoice)
def update_client_payment_due_date(sender, instance, created, **kwargs):
    if created:  # If the instance is being created
        client_payment = Payment.objects.get(user=instance.user, client=instance.client)
        client_payment.payment_due_date = instance.next_payment_due_date
        if instance.paid_fee:
            client_payment.paid_fee += instance.paid_fee
        client_payment.save()
