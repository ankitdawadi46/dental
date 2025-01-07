from django.core.exceptions import ValidationError
from django.db.models import F, IntegerField, Sum
from django.db.models.functions import Extract

from leave.domains import ILeaveLimitValidator
from leave.models import EmployeeLeave


class LeaveLimitValidator(ILeaveLimitValidator):
    """
    Validates that the requested leave does not exceed the annual leave limit.
    """

    def __init__(self, leave_type):
        self.leave_type = leave_type

    def validate(self, employee, start_date, end_date):
        if not self.leave_type.annual_leave_number:
            return  # No limit defined for this leave type

        total_days_requested = (end_date - start_date).days + 1

        # Calculate the total days already taken by the employee for this leave type
        total_leave_taken = (
            EmployeeLeave.objects.filter(
                employee=employee,
                leave_type=self.leave_type,
            )
            .annotate(total_duration=Extract(F("end_date") - F("start_date"), "day"))
            .aggregate(
                total_days=Sum(F("total_duration") + 1, output_field=IntegerField())
            )["total_days"]
            or 0
        )

        if (
            total_leave_taken + total_days_requested
            > self.leave_type.annual_leave_number
        ):
            raise ValidationError(
                f"This leave request exceeds the annual limit of {self.leave_type.annual_leave_number} days "
                f"for {self.leave_type.name}. You have already taken {total_leave_taken} days."
            )
