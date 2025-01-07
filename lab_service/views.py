from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from client.utils import with_tenant_context
from lab_service.models import LabService
from lab_service.serializers import LabServiceSerializer


class LabServiceViewSet(viewsets.ModelViewSet):
    queryset = LabService.objects.select_related("doctor").all()
    serializer_class = LabServiceSerializer
    permission_classes = [IsAuthenticated]
    
    @with_tenant_context
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @with_tenant_context
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @with_tenant_context
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

