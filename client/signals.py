import os
import uuid


from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django_tenants.models import TenantMixin, DomainMixin
from django_tenants_celery_beat.models import TenantTimezoneMixin
from accounts.models import User


@deconstructible
class RandomFileName(object):
    def __init__(self, path):
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _, filename):
        # @note It's up to the validators to check if it's the correct file type in name or if one even exist.
        extension = os.path.splitext(filename)[1]
        return self.path % (uuid.uuid4(), extension)


class DateTimeModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
    )
    updated_at = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
    )
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class ThemeTemplate(models.Model):
    name = models.CharField(max_length=1024)
    path_name = models.CharField(max_length=255)
    template_reference = models.ImageField(
        null=True, blank=True, upload_to=RandomFileName("template-preview")
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class SoftwareFeatures(DateTimeModel):
    name = models.CharField(max_length=255)
    identifier_slug = models.SlugField()

    def __str__(self):
        return self.name


class Client(TenantTimezoneMixin, TenantMixin):
    name = models.CharField(max_length=1024, verbose_name="business name")
    paid_until = models.DateTimeField()
    # campaign_id = models.IntegerField(blank=True, null=True)
    contact_person = models.CharField(null=True, blank=True, max_length=255)
    contact_number = models.CharField(null=True, blank=True, max_length=20)
    email = models.EmailField()
    template = models.ForeignKey(
        ThemeTemplate, null=True, blank=True, on_delete=models.SET_NULL
    )
    is_enabled = models.BooleanField(default=True)
    on_trial = models.BooleanField(default=False)
    primary_domain_name = models.CharField(null=True, blank=True, max_length=512)
    created_on = models.DateField(auto_now_add=True)
    initial_creation_handled = models.BooleanField(default=False)
    # default true, schema will be automatically created and synced when it is saved
    available_features = models.ManyToManyField(SoftwareFeatures, null=True, blank=True)
    auto_create_schema = True

    def get_client_url(self):
        return "https://{}".format(self.primary_domain_name)


class Domain(DomainMixin):
    ns_records = models.JSONField(null=True, blank=True)
    zone_id = models.CharField(max_length=512, null=True, blank=True)
    is_display_domain = models.BooleanField(default=False)

    def has_cf_configured(self):
        if self.zone_id:
            return True
        else:
            return False


class TemplateBlock(models.Model):
    name = models.CharField(max_length=250, unique=True)
    location = models.CharField(max_length=250)
    photo_reference = models.ImageField(
        upload_to=RandomFileName("template-block-reference"), blank=True, null=True
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class BlockTitle(models.Model):
    name = models.CharField(max_length=250, unique=True)
    location = models.CharField(max_length=250)
    photo_reference = models.ImageField(
        upload_to=RandomFileName("block-title-reference"), blank=True, null=True
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class TingTing(DateTimeModel):
    access_token = models.CharField(max_length=2000)
    refresh_token = models.CharField(max_length=2000)
    expires_at = models.DateTimeField()


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


from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save


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


class TingTingStatus(DateTimeModel):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    all_info = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.client.name} - {self.created_at.date()}"
