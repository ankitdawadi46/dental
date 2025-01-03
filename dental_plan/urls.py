from django.urls import path
from dental_plan.views import TenantConditionTreatmentView, DentalHistoryViewSet
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()

app_name = 'dental_plan'

routers.register(r'dental-history/(?P<tenant_schema_name>[^/.]+)', DentalHistoryViewSet, basename="dental_history")

urlpatterns = [
    path('plan/<str:tenant_schema_name>/', TenantConditionTreatmentView.as_view(), name='dental-plan'),
]

urlpatterns += routers.urls