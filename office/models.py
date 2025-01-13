from django.db import models
from client.models import AuditFields, CustomUser

# Create your models here.

class Company(AuditFields):
    logo = models.ImageField("logo", null=True, blank=True)
    name = models.CharField("Business Name", max_length=512)
    location = models.TextField("Address", null=True, blank=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=7, null=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=7, null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Company"


class OfficeHours(AuditFields):
    DAY_CHOICES = [
        (1, "Sunday"),
        (2, "Monday"),
        (3, "Tuesday"),
        (4, "Wednesday"),
        (5, "Thursday"),
        (6, "Friday"),
        (0, "Saturday"),
    ]

    day = models.IntegerField(choices=DAY_CHOICES, unique=True)
    is_active = models.BooleanField(default=False)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return (
            f"{self.get_day_display()} ({'Active' if self.is_active else 'Inactive'})"
        )

    class Meta:
        ordering = ["-day"]
        verbose_name = "Office Hour"
        verbose_name_plural = "Office Hour"


class OfficeHoliday(models.Model):
    name = models.CharField("Holiday Title", max_length=512)
    holiday_date = models.DateField("Holiday Date")
    allow_holiday = models.BooleanField(default=True)

    class Meta:
        ordering = ["-holiday_date"]
        verbose_name = "Office Holiday"
        verbose_name_plural = "Office Holiday"

    def __str__(self):
        return self.name