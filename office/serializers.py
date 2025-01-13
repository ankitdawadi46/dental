from rest_framework import serializers
from .models import Company, OfficeHours, OfficeHoliday


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class TimeSlotSerializer(serializers.Serializer):
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

    def validate(self, attrs):
        if attrs["start_time"] >= attrs["end_time"]:
            raise serializers.ValidationError("Start time must be before end time.")
        return attrs


class OfficeHourDaySerializer(serializers.Serializer):
    day = serializers.IntegerField()
    is_active = serializers.BooleanField(default=False)
    time_slots = TimeSlotSerializer(many=True)

    def validate_day(self, value):
        if value not in dict(OfficeHours.DAY_CHOICES):
            raise serializers.ValidationError("Invalid day choice.")
        return value


class BulkOfficeHoursSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    days = OfficeHourDaySerializer(many=True)

    def validate_employee_id(self, value):
        from client.models import CustomUser  # Adjust import as needed
        if not CustomUser.objects.filter(id=value).exists():
            raise serializers.ValidationError("Employee does not exist.")
        return value


class OfficeHolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeHoliday
        fields = "__all__"
