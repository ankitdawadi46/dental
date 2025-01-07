from django.urls import include, path
from rest_framework.routers import DefaultRouter

from lab_service.views import LabServiceViewSet

app_name = "lab_service"

router = DefaultRouter()
router.register(
    r"lab_service/(?P<tenant_schema_name>[^/.]+)",
    LabServiceViewSet,
    basename="lab-service",
)


urlpatterns = [
    path("", include(router.urls)),]