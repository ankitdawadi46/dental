from django.db import models

from client.models import AuditFields, CustomUser

# Create your models here.


class LeaveType(AuditFields):  # Add `AuditFields` if needed
    SICK_LEAVE = 'sick_leave'
    ANNUAL_LEAVE = 'annual_leave'
    UNPAID_LEAVE = 'unpaid_leave'

    LEAVE_TYPE_CHOICES = [
        (SICK_LEAVE, 'Sick Leave'),
        (ANNUAL_LEAVE, 'Annual Leave'),
        (UNPAID_LEAVE, 'Unpaid Leave'),
    ]

    DEFAULT_ANNUAL_LEAVE_NUMBERS = {
        SICK_LEAVE: 12,
        ANNUAL_LEAVE: 18,
        UNPAID_LEAVE: 30,
    }

    name = models.CharField(
        max_length=40,
        choices=LEAVE_TYPE_CHOICES,
        null=False,
        blank=False,
    )
    annual_leave_number = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.annual_leave_number is None and self.name in self.DEFAULT_ANNUAL_LEAVE_NUMBERS:
            self.annual_leave_number = self.DEFAULT_ANNUAL_LEAVE_NUMBERS[self.name]
        super().save(*args, **kwargs)


class EmployeeLeave(AuditFields):
    employee = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=False, blank=False
    )
    leave_type = models.ForeignKey(
        LeaveType, on_delete=models.CASCADE, null=True, blank=True
    )
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    is_admin_approved = models.BooleanField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
