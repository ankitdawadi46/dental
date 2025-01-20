from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaveTypeViewSet, EmployeeLeaveViewSet

app_name = 'leave'

router = DefaultRouter()
router.register(r'leave-types/(?P<tenant_schema_name>[^/.]+)', LeaveTypeViewSet, basename='leave-type')
router.register(r'employee-leaves', EmployeeLeaveViewSet, basename='employee-leave')

urlpatterns = [
    path('', include(router.urls)),
]