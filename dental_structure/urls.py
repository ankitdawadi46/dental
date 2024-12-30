from django.urls import path
from dental_structure.views import DentalStructureAPI

app_name = 'dental_structure'

urlpatterns = [
    path('structure/', DentalStructureAPI.as_view(), name='dental-structure'),
]