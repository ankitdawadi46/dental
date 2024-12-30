from django_tenants.utils import tenant_context
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from client.models import Client

from .models import Condition, Treatment
from .serializers import ConditionSerializer, TreatmentSerializer


class TenantConditionTreatmentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, tenant_schema_name):
        
        try:
            tenant = Client.objects.get(schema_name=tenant_schema_name)
        except Client.DoesNotExist:
            return Response({'error': 'Tenant not found'}, status=status.HTTP_404_NOT_FOUND)

        # Switch to the given tenant schema
        with tenant_context(tenant):
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

    def post(self, request, tenant_schema_name):
        try:
            tenant = Client.objects.get(schema_name=tenant_schema_name)
        except Client.DoesNotExist:
            return Response({'error': 'Tenant not found'}, status=status.HTTP_404_NOT_FOUND)
        # Switch to the given tenant schema
        with tenant_context(tenant):
            # Deserialize and create Condition
            condition_serializer = ConditionSerializer(
                data={'name': request.data.get("condition")})
            if condition_serializer.is_valid():
                condition_serializer.save()
            else:
                return Response(
                    condition_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            # Deserialize and create Treatment
            treatment_serializer = TreatmentSerializer(
                data={'name': request.data.get("treatment")}
            )
            if treatment_serializer.is_valid():
                treatment_serializer.save()
            else:
                return Response(
                    treatment_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {
                "condition": condition_serializer.data,
                "treatment": treatment_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
