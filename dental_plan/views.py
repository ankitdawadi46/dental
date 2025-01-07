from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from client.utils import atomic_transaction, with_tenant_context
from dental_app.utils.response import BaseResponse
from dental_plan.selectors.factories.dental_data_factory import DentalDataFactory
from dental_plan.selectors.factories.patient_full_dental_history import (
    DentalHistoryFactory,
)

from dental_plan.models import (
    Condition,
    DentalHistory,
    PatientCondition,
    PatientTreatment,
    Treatment,
)
from dental_plan.serializers import (
    ConditionSerializer,
    DentalHistoryPostSerializer,
    DentalHistorySerializer,
    PatientConditionSerializer,
    PatientTreatmentSerializer,
    TreatmentSerializer,
)


class TenantConditionTreatmentView(APIView):
    permission_classes = [AllowAny]

    @with_tenant_context
    @atomic_transaction
    def get(self, request, tenant_schema_name):
        conditions = Condition.objects.all()
        treatments = Treatment.objects.all()

        # Serialize the data
        condition_serializer = ConditionSerializer(conditions, many=True)
        treatment_serializer = TreatmentSerializer(treatments, many=True)

        return Response(
            {
                "conditions": condition_serializer.data,
                "treatments": treatment_serializer.data,
            }
        )

    @with_tenant_context
    @atomic_transaction
    def post(self, request, tenant_schema_name):
        # Deserialize and create Condition
        condition_serializer = ConditionSerializer(
            data={"name": request.data.get("condition")}
        )
        if condition_serializer.is_valid():
            condition_serializer.save()
        else:
            return BaseResponse(data=condition_serializer.errors, status=400)

        # Deserialize and create Treatment
        treatment_serializer = TreatmentSerializer(
            data={"name": request.data.get("treatment")}
        )
        if treatment_serializer.is_valid():
            treatment_serializer.save()
        else:
            return BaseResponse(data=treatment_serializer.errors, status=400)

        return BaseResponse(
            data={
                "condition": condition_serializer.data,
                "treatment": treatment_serializer.data,
            },
            status=201,
        )


class PatientConditionViewSet(viewsets.ModelViewSet):
    queryset = PatientCondition.objects.all()
    serializer_class = PatientConditionSerializer


class PatientTreatmentViewSet(viewsets.ModelViewSet):
    queryset = PatientTreatment.objects.all()
    serializer_class = PatientTreatmentSerializer


class DentalHistoryViewSet(viewsets.ModelViewSet):
    queryset = DentalHistory.objects.all()
    serializer_class = DentalHistoryPostSerializer
    permission_classes = [AllowAny]

    @with_tenant_context
    @atomic_transaction
    def create(self, request, tenant_schema_name, *args, **kwargs):
        data = request.data

        try:
            # Delegate to the coordinator
            result = DentalHistoryFactory.create_full_dental_history(data)

            # Serialize the response
            dental_history_serializer = self.get_serializer(result["dental_history"])
            patient_condition_serializer = PatientConditionSerializer(
                result["patient_condition"]
            )
            patient_treatment_serializer = PatientTreatmentSerializer(
                result["patient_treatment"]
            )

            return BaseResponse(
                data={
                    "dental_history": dental_history_serializer.data,
                    "patient_condition": patient_condition_serializer.data,
                    "patient_treatment": patient_treatment_serializer.data,
                },
                status=201,
            )

        except ObjectDoesNotExist as e:
            return BaseResponse(data={"error": str(e)}, status=400)
        except Exception as e:
            return BaseResponse(
                data={"error": "An unexpected error occurred", "details": str(e)},
                status=500,
            )

    @with_tenant_context
    @atomic_transaction
    def list(self, request, *args, **kwargs):
        patient_id = request.query_params.get("patient_id")
        dental_structure_id = request.query_params.get("dental_structure_id")

        if not patient_id or not dental_structure_id:
            return BaseResponse(
                data={"error": "patient_id and dental_structure_id are required."},
                status=400,
            )

        # Use factories to fetch data
        dental_history_factory = DentalDataFactory.get_dental_history_factory()
        condition_factory = DentalDataFactory.get_condition_factory()
        treatment_factory = DentalDataFactory.get_treatment_factory()

        dental_histories = dental_history_factory.dental_history_data(
            patient_id, dental_structure_id
        )

        if not dental_histories.exists():
            return BaseResponse(
                data={
                    "error": "No data found for the given patient and dental structure."
                },
                status=404,
            )

        # Serialize the dental histories
        dental_history_serializer = DentalHistorySerializer(dental_histories, many=True)

        # Fetch related conditions and treatments for patient data
        condition_ids = dental_histories.values_list("condition__id", flat=True)
        treatment_ids = dental_histories.values_list("treatment__id", flat=True)

        conditions = condition_factory.get_conditions(condition_ids)
        treatments = treatment_factory.get_treatments(treatment_ids)

        # Serialize patient conditions and treatments with nested data
        patient_condition_serializer = PatientConditionSerializer(conditions, many=True)
        patient_treatment_serializer = PatientTreatmentSerializer(treatments, many=True)

        return BaseResponse(
            data={
                "dental_histories": dental_history_serializer.data,
                "patient_conditions": patient_condition_serializer.data,
                "patient_treatments": patient_treatment_serializer.data,
            },
            status=200,
        )
