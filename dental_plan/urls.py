from django.urls import path
from rest_framework.routers import DefaultRouter

from dental_plan.views import (
    CompanyTreatmentProceduresViewset,
    TenantConditionTreatmentView,
    TreatmentMaterialUsedViewset,
)

routers = DefaultRouter()

app_name = "dental_plan"

# routers.register(
#     r"dental-history/(?P<tenant_schema_name>[^/.]+)",
#     DentalHistoryViewSet,
#     basename="dental_history",
# )
routers.register(
    r"company-treatment-plans",
    CompanyTreatmentProceduresViewset,
    basename="company_treatment_procedures",
)
# routers.register(
#     r"payment/(?P<tenant_schema_name>[^/.]+)", PaymentViewset, basename="payment"
# )
routers.register(
    r"material-used/(?P<tenant_schema_name>[^/.]+)",
    TreatmentMaterialUsedViewset,
    basename="treatment_material_used",
)

urlpatterns = [
    path(
        "plan/<str:tenant_schema_name>/",
        TenantConditionTreatmentView.as_view(),
        name="dental-plan",
    ),
]

urlpatterns += routers.urls
