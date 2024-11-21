from braces.views import LoginRequiredMixin

from django.urls import reverse_lazy
from django.contrib import messages


class BaseMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class CustomLoginRequiredmixin(LoginRequiredMixin):
    login_url = reverse_lazy("dashboard:login")


class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({"class": "form-control mb-3"})


class GetDeleteMixin:
    def get(self, request, *args, **kwargs):
        if hasattr(self, "success_message"):
            messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# from django_tenants_celery_beat.models import PeriodicTaskTenantLinkMixin

# class PeriodicTaskTenantLink(PeriodicTaskTenantLinkMixin):
#     pass
