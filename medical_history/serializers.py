from rest_framework import serializers
from .models import MedicalHistory, MedicalHistoryTypes


class MedicalHistoryTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistoryTypes
        fields = "__all__"


class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = "__all__"
