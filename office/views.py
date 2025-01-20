from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from client.utils import with_tenant_context
from dental_app.utils.response import BaseResponse
from office.models import Company, OfficeHoliday, OfficeHours
from office.selectors.office_hour_service import OfficeHoursService
from office.serializers import (
    BulkOfficeHoursSerializer,
    CompanySerializer,
    OfficeHolidaySerializer,
)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class OfficeHoursViewSet(viewsets.ModelViewSet):
    queryset = OfficeHours.objects.all()
    serializer_class = BulkOfficeHoursSerializer

    @action(detail=False, methods=["post"], url_path="bulk-create")
    def bulk_create(self, request, *args, **kwargs):
        """
        Custom action to create multiple OfficeHours with multiple time slots.
        """
        data = request.data  # Expecting a list of objects with employee_id and days
        if not isinstance(data, list):
            return BaseResponse(
                data={"detail": "Expected a list of objects."},
                status=400,
            )

        serializer = BulkOfficeHoursSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        # Prepare objects for bulk creation
        OfficeHoursService.create_bulk_office_hours(serializer.validated_data)

        return BaseResponse(
            data={"detail": "Office hours created successfully."},
            status=201,
        )


class OfficeHolidayViewSet(viewsets.ModelViewSet):
    queryset = OfficeHoliday.objects.all()
    serializer_class = OfficeHolidaySerializer

    # @with_tenant_context
    @action(
        detail=False,
        methods=["post"],
        url_path="bulk-create",
        permission_classes=[AllowAny],
    )
    def bulk_create(self, request, *args, **kwargs):
        """
        Custom action to create multiple office holidays in bulk.
        """
        data = request.data  # Expecting a list of holiday objects
        if not isinstance(data, list):
            return BaseResponse(
                data={"detail": "Expected a list of holiday objects."},
                status=400,
            )

        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_create(serializer)
        return BaseResponse(
            data=serializer.data,
            status=201,
        )

    def perform_bulk_create(self, serializer):
        """
        Performs bulk creation of holidays.
        """
        serializer.save()
