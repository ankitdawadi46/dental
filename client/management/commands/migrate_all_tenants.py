from django.core.management.base import BaseCommand
from django_tenants.utils import get_tenant_model
from django.core.management import call_command

class Command(BaseCommand):
    help = "Apply migrations to all tenants"

    def handle(self, *args, **options):
        TenantModel = get_tenant_model()
        for tenant in TenantModel.objects.all():
            print(tenant.schema_name)
            self.stdout.write(f"Applying migrations for {tenant.schema_name}...")
            if not tenant.schema_name == "Public":
                call_command("migrate_schemas", "--tenant", f"--schema={tenant.schema_name}")
        self.stdout.write(self.style.SUCCESS("Migrations applied to all tenants successfully!"))
