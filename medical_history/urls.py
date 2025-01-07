from django.urls import include, path
from rest_framework.routers import DefaultRouter

from medical_history.views import MedicalHistoryTypesViewSet, MedicalHistoryViewSet

app_name = "medical_history"

router = DefaultRouter()
router.register(
    r"medical-history-type/(?P<tenant_schema_name>[^/.]+)",
    MedicalHistoryTypesViewSet,
    basename="medical-history-types",
)
router.register(
    r"medical-history/(?P<tenant_schema_name>[^/.]+)",
    MedicalHistoryViewSet,
    basename="medical-history",
)

urlpatterns = [
    path("", include(router.urls)),
]
