from rest_framework import serializers
from lab_service.models import LabService


class LabServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabService
        fields = "__all__"