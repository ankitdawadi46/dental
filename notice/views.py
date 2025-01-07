from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from client.utils import with_tenant_context
from .models import Notice
from .serializers import NoticeSerializer

class NoticeViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing notices.
    """
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [AllowAny]  # Allow only authenticated users
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["organization", "is_active"]  # Enable filtering by organization and status
    search_fields = ["title", "content"]  # Enable search by title and content
    ordering_fields = ["created_at", "updated_at"]  # Allow ordering by creation/update time
    ordering = ["-created_at"]  # Default ordering by newest first
    
    @with_tenant_context
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @with_tenant_context
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @with_tenant_context
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
