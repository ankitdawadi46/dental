from django.core.exceptions import ValidationError

from leave.domains import ILeaveOverlapValidator
from leave.models import EmployeeLeave


class LeaveOverlapValidator(ILeaveOverlapValidator):
    """
    Validates that the requested leave period does not overlap with existing approved leave.
    """

    def __init__(self, leave_type):
        self.leave_type = leave_type

    def validate(self, employee, start_date, end_date, exclude_leave=None):
        # Check if the requested leave period overlaps with any previously approved leave
        overlapping_leave = EmployeeLeave.objects.filter(
            employee=employee,
            leave_type=self.leave_type,
            start_date__lte=end_date,  # Start date of existing leave is before or on the end date of new leave
            end_date__gte=start_date,  # End date of existing leave is after or on the start date of new leave
        ).exists()
        
        if exclude_leave:
            overlapping_leave = overlapping_leave.exclude(id=exclude_leave.id)

        if overlapping_leave:
            raise ValidationError(
                f"This leave request overlaps with an existing leave request for {self.leave_type.name}."
            )
