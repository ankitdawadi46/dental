from datetime import datetime

from django.forms import ValidationError
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from client.utils import with_tenant_context
from dental_app.utils.pagination import CustomPagination
from dental_app.utils.response import BaseResponse
from leave.models import EmployeeLeave, LeaveType
from leave.selectors.factories.leave_factory import LeaveFactory
from leave.serializers import EmployeeLeaveSerializer, LeaveTypeSerializer
from utils.get_employee import get_employee


class LeaveTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage leave types.
    Only admins can create, update, or delete leave types.
    """

    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [AllowAny]

    # @with_tenant_context
    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)

    # # @with_tenant_context
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    # @with_tenant_context
    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)

    # @with_tenant_context
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)


class EmployeeLeaveViewSet(viewsets.ModelViewSet):
    """
    API endpoint to handle employee leave requests.
    Employees can create leave requests.
    Admins can approve or reject leave requests.
    """

    queryset = EmployeeLeave.objects.all()
    serializer_class = EmployeeLeaveSerializer
    lookup_field = "id"  # Default primary key for the leave request
    lookup_url_kwarg = "leave_id"
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ["partial_update"]:
            # Only admins can approve/reject leave requests
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    # @with_tenant_context
    def create(self, request, *args, **kwargs):
        data = request.data

        # Extract and validate input data
        leave_type_id = data.get("leave_type")
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if not leave_type_id or not start_date or not end_date:
            return BaseResponse(
                data={"detail": "Leave type, start date, and end date are required."},
                status=400,
            )

        # Parse dates
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return BaseResponse(
                data={"detail": "Invalid date format. Use YYYY-MM-DD."}, status=400
            )

        # Get the leave type
        try:
            leave_type = LeaveType.objects.get(id=leave_type_id)
        except LeaveType.DoesNotExist:
            return BaseResponse(data={"detail": "Invalid leave type."}, status=400)

        # Initialize the leave service
        leave_service = LeaveFactory(leave_type)

        # Process the leave request
        try:
            leave_request = leave_service.handle_leave_request(
                employee=get_employee(request, data),
                validated_data={
                    "leave_type": leave_type,
                    "start_date": start_date,
                    "end_date": end_date,
                },
            )
        except ValidationError as e:
            return BaseResponse(data={"detail": str(e)}, status=400)

        # Serialize and return the created leave request
        serializer = EmployeeLeaveSerializer(leave_request)
        return BaseResponse(data=serializer.data, status=201)
    
    # @with_tenant_context
    def partial_update(self, request, *args, **kwargs):
        leave_id = kwargs.get(self.lookup_url_kwarg)  # Extract leave_id from URL parameters

        # Fetch the leave request to update
        try:
            leave_request = EmployeeLeave.objects.get(id=leave_id)
        except EmployeeLeave.DoesNotExist:
            return BaseResponse(
                data={"detail": "Leave request not found."},
                status=404,
            )

        # Check if the request data has `is_admin_approved`
        is_admin_approved = request.data.get("is_admin_approved")
        if is_admin_approved is None:
            return BaseResponse(
                data={"detail": "is_admin_approved field is required."},
                status=400,
            )


        # Update the field
        leave_request.is_admin_approved = is_admin_approved
        leave_request.save()

        # Serialize and return the updated leave request
        serializer = self.get_serializer(leave_request)
        return BaseResponse(data=serializer.data, status=200)

    # @with_tenant_context
    def update(self, request, *args, **kwargs):
        leave_id = kwargs.get(
            self.lookup_url_kwarg
        )  # Extract leave_id from URL parameters
        data = request.data

        # Extract and validate input data
        leave_type_id = data.get("leave_type")
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if not leave_type_id or not start_date or not end_date:
            return BaseResponse(
                data={"detail": "Leave type, start date, and end date are required."},
                status=400,
            )

        # Parse dates
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return BaseResponse(
                data={"detail": "Invalid date format. Use YYYY-MM-DD."},
                status=400,
            )

        # Get the leave type
        try:
            leave_type = LeaveType.objects.get(id=leave_type_id)
        except LeaveType.DoesNotExist:
            return BaseResponse(
                data={"detail": "Invalid leave type."},
                status=400,
            )

        # Fetch the leave request to update
        try:
            leave_request = EmployeeLeave.objects.get(
                id=leave_id, employee=get_employee(request, data)
            )
        except EmployeeLeave.DoesNotExist:
            return BaseResponse(
                data={"detail": "Leave request not found."},
                status=404,
            )

        # Initialize the LeaveFactory
        leave_service = LeaveFactory(leave_type)

        # Process the leave update
        try:
            # Pass existing leave to exclude it during validation
            leave_service.leave_validator.validate_leave_request(
                employee=get_employee(request, data),
                start_date=start_date,
                end_date=end_date,
                exclude_leave=leave_request,  # Prevent overlap with itself
            )

            # Update leave request
            validated_data = {
                "leave_type": leave_type,
                "start_date": start_date,
                "end_date": end_date,
            }
            leave_request = leave_service.leave_creator.update_leave(
                leave_request=leave_request, validated_data=validated_data
            )

        except ValidationError as e:
            return BaseResponse(
                data={"detail": str(e)},
                status=400,
            )

        # Serialize and return the updated leave request
        serializer = self.get_serializer(leave_request)
        return BaseResponse(data=serializer.data, status=200)
    
    # @with_tenant_context
    def list(self, request, *args, **kwargs):
        """
        Retrieve all leave requests for the currently authenticated employee.
        """
        # Call the original list method to get the default queryset
        queryset = self.filter_queryset(self.get_queryset())

        # Pagination (optional, you can customize how it works if needed)
        page = self.paginate_queryset(queryset)
        if page is not None:
            # You can customize the paginated response format here
            serializer = self.get_serializer(page, many=True)
            return BaseResponse(
                data=self.get_paginated_response(serializer.data).data,  # You can change this response structure
                status=200
            )

        # Serialize the queryset without pagination (fallback)
        serializer = self.get_serializer(queryset, many=True)
        return BaseResponse(data=serializer.data, status=200)
        
    # @with_tenant_context
    def retrieve(self, request, *args, **kwargs):
        employee_id = kwargs.get(self.lookup_url_kwarg, None)
        """
        Retrieve all leave requests for the currently authenticated employee.
        """
        # Filter leave requests by the logged-in user
        if request.user.is_staff:
            leaves = EmployeeLeave.objects.all(employee=employee_id)
        else:
            leaves = EmployeeLeave.objects.filter(employee=request.user)

        page = self.paginate_queryset(leaves)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return BaseResponse(
                data=self.get_paginated_response(serializer.data).data,
                status=200)

        # Serialize the data without pagination (fallback)
        serializer = self.get_serializer(leaves, many=True)
        return BaseResponse(data=serializer.data, status=200)



