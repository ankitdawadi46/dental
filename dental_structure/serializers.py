from rest_framework.serializers import ModelSerializer

from dental_structure.models import (
    DentalDiagnosis,
    DentalDiagnosisProcedures,
    DentalDiagnosisTypes,
    DentalStructure,
    DentalTreatmentProcedures,
    DentalTreatments,
    DentalTreatmentTypes,
)


class DentalTreatmentsSerializer(ModelSerializer):
    class Meta:
        model = DentalTreatments
        fields = "__all__"


class DentalTreatmentTypesSerializer(ModelSerializer):
    class Meta:
        model = DentalTreatmentTypes
        fields = "__all__"


class DentalTreatmentProceduresSerializer(ModelSerializer):
    class Meta:
        model = DentalTreatmentProcedures
        fields = "__all__"


class DentalDiagnosisSerializer(ModelSerializer):
    class Meta:
        model = DentalDiagnosis
        fields = "__all__"


class DentalDiagnosisTypesSerializer(ModelSerializer):
    class Meta:
        model = DentalDiagnosisTypes
        fields = "__all__"


class DentalDiagnosisProceduresSerializer(ModelSerializer):
    class Meta:
        model = DentalDiagnosisProcedures
        fields = "__all__"
        

class DentalStructureSerializer(ModelSerializer):
    
    class Meta:
        model = DentalStructure
        fields = "__all__"
