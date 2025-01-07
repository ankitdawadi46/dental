from leave.domains import ILeaveFactory
from leave.selectors.leave_creator import LeaveCreator
from leave.selectors.leave_validator import LeaveValidator


class LeaveFactory(ILeaveFactory):
    """
    Abstract Factory for creating leave-related services.
    """

    def __init__(self, leave_type):
        self.leave_type = leave_type
        self.leave_validator = LeaveValidator(leave_type)
        self.leave_creator = LeaveCreator()

    def handle_leave_request(self, employee, validated_data):
        """
        Handles the entire leave request process: validation and creation.
        """
        # Validate the leave request
        self.leave_validator.validate_leave_request(
            employee=employee,
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
        )

        # Create the leave request
        leave_request = self.leave_creator.create_leave(
            employee=employee, validated_data=validated_data
        )

        return leave_request
