from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from dental_app.utils.response import BaseResponse
from dental_structure.models import DentalStructure, DentalTreatments
from dental_structure.selectors.factory.dental_flattened_plan import DentalTreatmentFactory
from dental_structure.serializers import DentalTreatmentsSerializer


class DentalStructureAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = []
        structures = DentalStructure.objects.prefetch_related("roots").all()
        for structure in structures:
            data.append(
                {
                    "name": structure.name,
                    "tooth_type": structure.tooth_type,
                    "quadrant": structure.quadrant,
                    "num_roots": structure.num_roots,
                    "d3_points": structure.d3_points,
                    "roots": [
                        {"name": root.name, "d3_points": root.d3_points}
                        for root in structure.roots.all()
                    ],
                }
            )
        return BaseResponse(data=data, status=200)


class DentalTreatmentViewset(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = DentalTreatments.objects.all()
    serializer_class = DentalTreatmentsSerializer

    @action(detail=False, methods=["get"])
    def get_flattened_dental_treatment(self, request):
        """
        Returns a flattened list of dental treatments, types, and procedures.
        """
        flattened_data = DentalTreatmentFactory.get_flattened_dental_treatments()
        return BaseResponse(data=flattened_data, status=200)
