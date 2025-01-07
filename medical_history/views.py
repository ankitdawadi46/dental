from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from client.utils import with_tenant_context
from dental_app.utils.permissions import IsClient, IsDoctor

from .models import MedicalHistory, MedicalHistoryTypes
from .serializers import MedicalHistorySerializer, MedicalHistoryTypesSerializer


class MedicalHistoryTypesViewSet(viewsets.ModelViewSet):
    queryset = MedicalHistoryTypes.objects.all()
    serializer_class = MedicalHistoryTypesSerializer
    permission_classes = [IsClient]
    
    @with_tenant_context
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @with_tenant_context
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @with_tenant_context
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @with_tenant_context
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class MedicalHistoryViewSet(viewsets.ModelViewSet):
    queryset = MedicalHistory.objects.select_related(
        "patient", "medical_history_type"
    ).all()
    serializer_class = MedicalHistorySerializer
    permission_classes = [IsDoctor]
    
    @with_tenant_context
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @with_tenant_context
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @with_tenant_context
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @with_tenant_context
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

