from rest_framework import serializers
from .models import Condition, DentalHistory, PatientCondition, PatientTreatment, Treatment

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ['id', 'name']


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ['id', 'name']
        
        
class PatientConditionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PatientCondition
        fields = '__all__'
        

class PatientTreatmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PatientTreatment
        fields = "__all__"
        

class PatientConditionNestedSerializer(serializers.ModelSerializer):
    condition = ConditionSerializer()
    treatment = TreatmentSerializer()

    class Meta:
        model = PatientCondition
        fields = ["id", "name", "description", "condition", "treatment", "severity", "d3_image"]


class PatientTreatmentNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientTreatment
        fields = ["id", "name", "description", "material_used", "d3_image"]
        

class DentalHistoryPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = DentalHistory
        fields = '__all__'
        

class DentalHistorySerializer(serializers.ModelSerializer):
    condition = ConditionSerializer()
    treatment = TreatmentSerializer()

    class Meta:
        model = DentalHistory
        fields = [
            "id",
            "patient",
            "dental_structure",
            "date",
            "condition",
            "treatment",
            "notes",
        ]
        


