from django.urls import path
from rest_framework.routers import DefaultRouter
from dental_structure.views import DentalStructureAPI, DentalTreatmentViewset

app_name = 'dental_structure'

router = DefaultRouter()

router.register(r"dental-treatment", DentalTreatmentViewset, "dental_treatment")

urlpatterns = [
    path('structure/', DentalStructureAPI.as_view(), name='dental-structure'),
]

urlpatterns += router.urls