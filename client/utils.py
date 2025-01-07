from functools import wraps

from django.db import transaction

# from myapp.models import Client  # Adjust the import based on your app
from django_tenants.utils import tenant_context

from dental_app.utils.response import BaseResponse

from .models import Client


def hostname_from_request(request):
    """returns hosts name from request"""
    return request.get_host().split(":")[0].lower()


def root_company():
    return Client.objects.filter(schema_name="public").first()


def company_from_request(request):
    """returns company from current request"""
    if hasattr(request, "cache__company"):
        return request.cache__company

    hostname = hostname_from_request(request)
    # print(hostname)
    company = Client.objects.filter(domain_url=hostname).first()
    setattr(request, "cache__company", company)
    return company


def get_company_domain(request):
    company = company_from_request(request)
    if company:
        return company.domain_url
    else:
        return root_company().domain_url


def get_company_url(request):
    company = company_from_request(request)
    if company:
        if request.is_secure():
            return "https://" + company.domain_url
        return "http://" + company.domain_url
    else:
        return root_company().domain_url


# Assuming `tenant_context` is already implemente
def with_tenant_context(func):
    @wraps(func)
    def wrapper(self, request, tenant_schema_name, *args, **kwargs):
        try:
            tenant = Client.objects.get(schema_name=tenant_schema_name)
        except Client.DoesNotExist:
            return BaseResponse(data={"error": "Tenant not found"}, status=404)

        # Switch to the given tenant schema
        with tenant_context(tenant):
            return func(self, request, tenant_schema_name, *args, **kwargs)

    return wrapper


def atomic_transaction(func):
    """
    Decorator to wrap a function within a transaction.atomic block.
    Rolls back the transaction if any exception is raised.
    """

    def wrapper(*args, **kwargs):
        with transaction.atomic():
            return func(*args, **kwargs)

    return wrapper
