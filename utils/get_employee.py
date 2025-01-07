from client.models import CustomUser
from dental_app.utils.response import BaseResponse


def get_employee(request, data):
    if request.user.is_staff:
        employee_id = data.get('employee_id')
        if not employee_id:
            return BaseResponse(
                data={"detail": "Employee ID is required for staff."},
                status=400,
            )
        try:
            employee = CustomUser.objects.get(id=employee_id)
        except CustomUser.DoesNotExist:
            return BaseResponse(
                data={"detail": "Employee not found."},
                status=404,
            )
    else:
        employee = request.user
    return employee