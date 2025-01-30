from rest_framework import serializers

from client.serializers import CustomUserSerializer
from dental_plan.models import (
    CompanyTreamentProcedureSession,
    CompanyTreatmentProcedures,
    PatientDentalTreatmentPlans,
    TreatmentMaterialUsed,
    CompanyDiagnosticProcedures
)
from dental_structure.serializers import DentalStructureSerializer

# class ConditionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Condition
#         fields = ["id", "name"]


# class TreatmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Treatment
#         fields = ["id", "name"]


# class PatientConditionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PatientCondition
#         fields = "__all__"


# class PatientTreatmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PatientTreatment
#         fields = "__all__"


# class PatientConditionNestedSerializer(serializers.ModelSerializer):
#     condition = ConditionSerializer()
#     treatment = TreatmentSerializer()

#     class Meta:
#         model = PatientCondition
#         fields = [
#             "id",
#             "name",
#             "description",
#             "condition",
#             "treatment",
#             "severity",
#             "d3_image",
#         ]


# class PatientTreatmentNestedSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PatientTreatment
#         fields = ["id", "name", "description", "material_used", "d3_image"]


# class DentalHistoryPostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DentalHistory
#         fields = "__all__"


# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = "__all__"


# class DentalHistorySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = DentalHistory
#         fields = [
#             "id",
#             "patient",
#             "dental_structure",
#             "date",
#             "condition",
#             "treatment",
#             "notes",
#         ]


class TreatmentMaterialsUsedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentMaterialUsed
        fields = "__all__"


class CompanyTreatmentProcedureSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyTreamentProcedureSession
        fields = "__all__"


class CompanyTreatmentProceduresSerializer(serializers.ModelSerializer):
    company_treatment_procedure_sessions = CompanyTreatmentProcedureSessionSerializer(
        many=True, required=True
    )
    treatment_material_used = TreatmentMaterialsUsedSerializer(many=True, required=True)

    class Meta:
        model = CompanyTreatmentProcedures
        fields = [
            "id",
            "service_type_id",
            "procedure_id",
            "procedure_name",
            "service_type_name",
            "price",
            "company_treatment_procedure_sessions",
            "treatment_material_used",
        ]
        

class CompanyDiagnosticProceduresSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CompanyDiagnosticProcedures
        fields = "__all__"
        

class PatientDentalTreatmentPlanSerializer(serializers.ModelSerializer):
     
    class Meta:
         model = PatientDentalTreatmentPlans
         fields = "__all__"
         
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['patient'] = CustomUserSerializer(instance.patient).data
        response['dental_structure'] = DentalStructureSerializer(instance.dental_structure).data
        response['dental_procedures'] = CompanyTreatmentProceduresSerializer(instance.dental_procedures).data
        return response
