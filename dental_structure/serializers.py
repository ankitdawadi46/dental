from rest_framework.serializers import ModelSerializer

from dental_structure.models import DentalTreatments


class DentalTreatmentsSerializer(ModelSerializer):
    
    class Meta:
        model = DentalTreatments
        fields = "__all__"