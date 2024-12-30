from django.urls import path
from dental_plan.views import TenantConditionTreatmentView

app_name = 'dental_plan'

urlpatterns = [
    path('plan/<str:tenant_schema_name>/', TenantConditionTreatmentView.as_view(), name='dental-plan'),
]