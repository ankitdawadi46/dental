from rest_framework.routers import DefaultRouter

from office.views import OfficeHolidayViewSet

app_name = "office"

router = DefaultRouter()
router.register(
    r"office-holiday/(?P<tenant_schema_name>[^/.]+)", OfficeHolidayViewSet, basename="office_holiday"
)

urlpatterns = [] + router.urls
