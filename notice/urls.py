from rest_framework.routers import DefaultRouter
from .views import NoticeViewSet


app_name = 'notice'

router = DefaultRouter()
router.register(r"notices/(?P<tenant_schema_name>[^/.]+)", NoticeViewSet, basename="notice")

urlpatterns = [] + router.urls