from leave.domains import ILeaveValidator
from leave.selectors.leave_limit_validator import LeaveLimitValidator
from leave.selectors.leave_overlap_validator import LeaveOverlapValidator


class LeaveValidator(ILeaveValidator):
    """
    Coordinates the validation of a leave request.
    """

    def __init__(self, leave_type):
        self.leave_type = leave_type
        self.leave_limit_validator = LeaveLimitValidator(leave_type)
        self.leave_overlap_validator = LeaveOverlapValidator(leave_type)

    def validate_leave_request(self, employee, start_date, end_date, exclude_leave=None):
        # Validate the annual leave limit
        self.leave_limit_validator.validate(employee, start_date, end_date)

        # Validate the overlapping leave requests
        self.leave_overlap_validator.validate(employee, start_date, end_date, exclude_leave=None)