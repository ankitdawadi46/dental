from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from dental_app.utils.response import BaseResponse
from dental_structure.models import (
    DentalDiagnosis,
    DentalDiagnosisProcedures,
    DentalDiagnosisTypes,
    DentalStructure,
    DentalTreatmentProcedures,
    DentalTreatments,
    DentalTreatmentTypes,
)
from dental_structure.selectors.factory.dental_flattened_plan import (
    DentalTreatmentFactory,
)
from dental_structure.serializers import (
    DentalDiagnosisProceduresSerializer,
    DentalDiagnosisSerializer,
    DentalDiagnosisTypesSerializer,
    DentalStructureSerializer,
    DentalTreatmentProceduresSerializer,
    DentalTreatmentsSerializer,
    DentalTreatmentTypesSerializer,
)


class DentalStructureViewSet(ModelViewSet):
    queryset = DentalStructure.objects.all().order_by("dental_numbering")
    serializer_class = DentalStructureSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ["dental_numbering"]


class DentalTreatmentViewset(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = DentalTreatments.objects.all()
    serializer_class = DentalTreatmentsSerializer
    filter_backends = DjangoFilterBackend

    @action(detail=False, methods=["get"])
    def get_flattened_dental_treatment(self, request):
        """
        Returns a flattened list of dental treatments, types, and procedures.
        """
        flattened_data = DentalTreatmentFactory.get_flattened_dental_treatments()
        return BaseResponse(data=flattened_data, status=200)


class DentalTreatmentTypesViewSet(ModelViewSet):
    queryset = DentalTreatmentTypes.objects.all()
    serializer_class = DentalTreatmentTypesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [AllowAny]
    filterset_fields = ["service_type_name", "service_name"]
    search_fields = ["service_type_name", "service_description"]
    ordering_fields = ["service_type_name", "id"]


class DentalTreatmentProceduresViewSet(ModelViewSet):
    queryset = DentalTreatmentProcedures.objects.all()
    serializer_class = DentalTreatmentProceduresSerializer


class DentalDiagnosisViewSet(ModelViewSet):
    queryset = DentalDiagnosis.objects.all()
    serializer_class = DentalDiagnosisSerializer
    permission_classes = [AllowAny]


class DentalDiagnosisTypesViewSet(ModelViewSet):
    queryset = DentalDiagnosisTypes.objects.all()
    serializer_class = DentalDiagnosisTypesSerializer
    permission_classes = [AllowAny]


class DentalDiagnosisProceduresViewSet(ModelViewSet):
    queryset = DentalDiagnosisProcedures.objects.all()
    serializer_class = DentalDiagnosisProceduresSerializer
