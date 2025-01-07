from rest_framework import serializers
from leave.models import LeaveType, EmployeeLeave


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = ['id', 'name', 'annual_leave_number']


class EmployeeLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLeave
        fields = [
            'id',
            'employee',
            'leave_type',
            'start_date',
            'end_date',
            'is_admin_approved',
            'description',
        ]
        read_only_fields = ['is_admin_approved']