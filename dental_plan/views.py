from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from dental_app.utils.response import BaseResponse
from dental_plan.models import (
    CompanyTreatmentProcedures,
    TreatmentMaterialUsed,
    CompanyDiagnosticProcedures
)
from dental_plan.selectors.factories.treatment_procedure_factory import (
    TreatmentProcedureFactory,
)
from dental_plan.serializers import (
    CompanyTreatmentProceduresSerializer,
    TreatmentMaterialsUsedSerializer,
    CompanyDiagnosticProceduresSerializer
)

# class TenantConditionTreatmentView(APIView):
#     permission_classes = [AllowAny]

#     # @with_tenant_context
#     @atomic_transaction
#     def get(self, request, tenant_schema_name):
#         conditions = Condition.objects.all()
#         treatments = Treatment.objects.all()

#         # Serialize the data
#         condition_serializer = ConditionSerializer(conditions, many=True)
#         treatment_serializer = TreatmentSerializer(treatments, many=True)

#         return Response(
#             {
#                 "conditions": condition_serializer.data,
#                 "treatments": treatment_serializer.data,
#             }
#         )

#     # @with_tenant_context
#     @atomic_transaction
#     def post(self, request, tenant_schema_name):
#         # Deserialize and create Condition
#         condition_serializer = ConditionSerializer(
#             data={"name": request.data.get("condition")}
#         )
#         if condition_serializer.is_valid():
#             condition_serializer.save()
#         else:
#             return BaseResponse(data=condition_serializer.errors, status=400)

#         # Deserialize and create Treatment
#         treatment_serializer = TreatmentSerializer(
#             data={"name": request.data.get("treatment")}
#         )
#         if treatment_serializer.is_valid():
#             treatment_serializer.save()
#         else:
#             return BaseResponse(data=treatment_serializer.errors, status=400)

#         return BaseResponse(
#             data={
#                 "condition": condition_serializer.data,
#                 "treatment": treatment_serializer.data,
#             },
#             status=201,
#         )


# class PatientConditionViewSet(viewsets.ModelViewSet):
#     queryset = PatientCondition.objects.all()
#     serializer_class = PatientConditionSerializer


# class PatientTreatmentViewSet(viewsets.ModelViewSet):
#     queryset = PatientTreatment.objects.all()
#     serializer_class = PatientTreatmentSerializer


# class PaymentViewset(viewsets.ModelViewSet):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer
#     permission_classes = [AllowAny]

# @with_tenant_context
# def list(self, request, *args, **kwargs):
#     return super().list(request, *args, **kwargs)

# @with_tenant_context
# def create(self, request, *args, **kwargs):
#     return super().create(request, *args, **kwargs)

# @with_tenant_context
# def update(self, request, *args, **kwargs):
#     return super().update(request, *args, **kwargs)

# @with_tenant_context
# def destroy(self, request, *args, **kwargs):
#     return super().destroy(request, *args, **kwargs)


class TreatmentMaterialUsedViewset(viewsets.ModelViewSet):
    queryset = TreatmentMaterialUsed.objects.all()
    serializer_class = TreatmentMaterialsUsedSerializer
    permission_classes = [AllowAny]

    # # @with_tenant_context
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    # # @with_tenant_context
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    # # @with_tenant_context
    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)

    # @with_tenant_context
    def destroy(self, request, *args, **kwargs):
        # Retrieve the object safely
        instance = self.get_object_or_404_instance(kwargs)

        # Perform the delete operation
        self.perform_destroy(instance)

        # Return a success response
        return BaseResponse(data={"detail": "Object deleted successfully."}, status=204)

    def perform_destroy(self, instance):
        """
        Perform the actual deletion of the instance.
        You can customize this if you need any pre-delete or post-delete logic.
        """
        instance.delete(hard=True)

    def get_object_or_404_instance(self, kwargs):
        """
        Retrieves the object using get_object() or get_object_or_404.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Pass kwargs to filter the object
        lookup_url_kwarg = self.lookup_field  # Typically 'pk'
        filter_kwargs = {self.lookup_field: kwargs.get(lookup_url_kwarg)}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # Check for object permissions
        self.check_object_permissions(self.request, obj)

        return obj


# class DentalHistoryViewSet(viewsets.ModelViewSet):
#     queryset = DentalHistory.objects.all()
#     serializer_class = DentalHistoryPostSerializer
#     permission_classes = [AllowAny]

#     # @with_tenant_context
#     @atomic_transaction
#     def create(self, request, tenant_schema_name, *args, **kwargs):
#         data = request.data

#         try:
#             # Delegate to the coordinator
#             result = DentalHistoryFactory.create_full_dental_history(data)

#             # Serialize the response
#             dental_history_serializer = self.get_serializer(result["dental_history"])
#             patient_condition_serializer = PatientConditionSerializer(
#                 result["patient_condition"]
#             )
#             patient_treatment_serializer = PatientTreatmentSerializer(
#                 result["patient_treatment"]
#             )

#             return BaseResponse(
#                 data={
#                     "dental_history": dental_history_serializer.data,
#                     "patient_condition": patient_condition_serializer.data,
#                     "patient_treatment": patient_treatment_serializer.data,
#                 },
#                 status=201,
#             )

#         except ObjectDoesNotExist as e:
#             return BaseResponse(data={"error": str(e)}, status=400)
#         except Exception as e:
#             return BaseResponse(
#                 data={"error": "An unexpected error occurred", "details": str(e)},
#                 status=500,
#             )

#     # @with_tenant_context
#     @atomic_transaction
#     def list(self, request, *args, **kwargs):
#         patient_id = request.query_params.get("patient_id")
#         dental_structure_id = request.query_params.get("dental_structure_id")

#         if not patient_id or not dental_structure_id:
#             return BaseResponse(
#                 data={"error": "patient_id and dental_structure_id are required."},
#                 status=400,
#             )

#         # Use factories to fetch data
#         dental_history_factory = DentalDataFactory.get_dental_history_factory()
#         condition_factory = DentalDataFactory.get_condition_factory()
#         treatment_factory = DentalDataFactory.get_treatment_factory()
#         payment_factory = DentalDataFactory.get_payment_factory()

#         dental_histories = dental_history_factory.dental_history_data(
#             patient_id, dental_structure_id
#         )

#         if not dental_histories.exists():
#             return BaseResponse(
#                 data={
#                     "error": "No data found for the given patient and dental structure."
#                 },
#                 status=404,
#             )

#         # Serialize the dental histories
#         dental_history_serializer = DentalHistorySerializer(dental_histories, many=True)
#         # Fetch related conditions and treatments for patient data
#         condition_ids = dental_histories.values_list("condition__id", flat=True)
#         treatment_ids = dental_histories.values_list("treatment__id", flat=True)

#         conditions = condition_factory.get_conditions(condition_ids)
#         treatments = treatment_factory.get_treatments(treatment_ids)
#         payments = payment_factory.get_payments(treatment_ids)

#         # Serialize patient conditions and treatments with nested data
#         patient_condition_serializer = PatientConditionSerializer(conditions, many=True)
#         patient_treatment_serializer = PatientTreatmentSerializer(treatments, many=True)
#         payments = PaymentSerializer(payments, many=True)

#         return BaseResponse(
#             data={
#                 "dental_histories": dental_history_serializer.data,
#                 "patient_conditions": patient_condition_serializer.data,
#                 "patient_treatments": patient_treatment_serializer.data,
#                 "payments": payments.data
#             },
#             status=200,
#         )


class CompanyTreatmentProceduresViewset(viewsets.ModelViewSet):
    queryset = CompanyTreatmentProcedures.objects.all()
    serializer_class = CompanyTreatmentProceduresSerializer
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.factory = TreatmentProcedureFactory()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Delegate creation to the factory
        company_treatment_procedure = self.factory.create(serializer.validated_data)
        response_serializer = self.get_serializer(company_treatment_procedure)
        return BaseResponse(data=response_serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        # Delegate update to the factory
        company_treatment_procedure = self.factory.update(
            instance, serializer.validated_data
        )
        response_serializer = self.get_serializer(company_treatment_procedure)
        return BaseResponse(data=response_serializer.data, status=200)
    

class CompanyDiagnosticProceduresViewset(viewsets.ModelViewSet):
    queryset = CompanyDiagnosticProcedures.objects.all()
    serializer_class = CompanyDiagnosticProceduresSerializer
    permission_classes = [AllowAny]
