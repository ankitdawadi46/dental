from leave.domains import ILeaveCreator
from leave.models import EmployeeLeave


class LeaveCreator(ILeaveCreator):
    """
    Handles creation of the leave record after validation.
    """

    def create_leave(self, employee, validated_data):
        """
        Create the leave request after validation.
        """
        validated_data = validated_data.copy()  # Make a mutable copy
        validated_data["employee"] = employee  # Now you can modify it
        employee_leave = EmployeeLeave()
        employee_leave.employee = validated_data["employee"]
        employee_leave.leave_type = validated_data["leave_type"]
        employee_leave.start_date = validated_data["start_date"]
        employee_leave.end_date = validated_data["end_date"]
        employee_leave.save()
        return employee_leave
    
    def update_leave(self, leave_request, validated_data):
        leave_request.leave_type = validated_data["leave_type"]
        leave_request.start_date = validated_data["start_date"]
        leave_request.end_date = validated_data["end_date"]
        leave_request.save()
        return leave_request