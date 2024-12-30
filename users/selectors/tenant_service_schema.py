from django_tenants.utils import schema_context

class TenantService:
    def switch_to_tenant_schema(self, tenant_schema_name):
        with schema_context(tenant_schema_name):
            # Logic to ensure the tenant schema switch is successful (e.g., check the connection)
            pass