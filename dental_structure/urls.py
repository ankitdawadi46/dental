from django.urls import path
from rest_framework.routers import DefaultRouter
from dental_structure.views import DentalDiagnosisProceduresViewSet, DentalDiagnosisTypesViewSet, DentalDiagnosisViewSet, DentalStructureAPI, DentalTreatmentProceduresViewSet, DentalTreatmentTypesViewSet, DentalTreatmentViewset

app_name = 'dental_structure'

router = DefaultRouter()

router.register(r"dental-treatment", DentalTreatmentViewset, "dental_treatment")
router.register(r"dental-treatment-types", DentalTreatmentTypesViewSet)
router.register(r"dental-treatment-procedures", DentalTreatmentProceduresViewSet)
router.register(r"dental-diagnosis", DentalDiagnosisViewSet)
router.register(r"dental-diagnosis-types", DentalDiagnosisTypesViewSet)
router.register(r"dental-diagnosis-procedures", DentalDiagnosisProceduresViewSet)

urlpatterns = [
    path('structure/', DentalStructureAPI.as_view(), name='dental-structure'),
]

urlpatterns += router.urls