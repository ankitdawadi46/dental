from dental_app.utils.response import BaseResponse
from dental_structure.models import DentalStructure
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class DentalStructureAPI(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        data = []
        structures = DentalStructure.objects.prefetch_related('roots').all()
        for structure in structures:
            data.append({
                "name": structure.name,
                "tooth_type": structure.tooth_type,
                "quadrant": structure.quadrant,
                "num_roots": structure.num_roots,
                "d3_points": structure.d3_points,
                "roots": [
                    {
                        "name": root.name,
                        "d3_points": root.d3_points
                    } for root in structure.roots.all()
                ]
            })
        return BaseResponse(
            data=data,
            status=200)
