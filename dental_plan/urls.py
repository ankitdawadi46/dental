from rest_framework.routers import DefaultRouter

from dental_plan.views import (
    CompanyTreatmentProceduresViewset,
    PatientDentalTreatmentPlanViewset,
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
routers.register(
    r"patient-dental-treatment-plans", PatientDentalTreatmentPlanViewset,
    basename="patient_dental_treatment_plans"
)
# routers.register(
#     r"company-diagnostic-procedure", 
# )

urlpatterns = [
    # path(
    #     "plan/<str:tenant_schema_name>/",
    #     TenantConditionTreatmentView.as_view(),
    #     name="dental-plan",
    # ),
]

urlpatterns += routers.urls
