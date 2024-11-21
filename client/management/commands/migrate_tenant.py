from concurrent.futures import ThreadPoolExecutor, as_completed
from django.core.management.base import BaseCommand
from tenant_schemas.utils import get_tenant_model

from django.core.management import call_command
from tenant_schemas.utils import schema_context


def migrate_tenant(tenant):
    """
    Migrates the database schema for a single tenant.

    :param tenant: The tenant instance to migrate.
    """
    # print(tenant)
    try:
        # Set the schema context for the current tenant.
        # This ensures that the migrations apply to the correct tenant schema.
        with schema_context(tenant.schema_name):
            # Run the migrate_schemas command for the tenant.
            # Specify any additional arguments or options as needed.
            call_command(
                "migrate_schemas",
                schema_name=tenant.schema_name,
                verbosity=1,
                interactive=False,
            )

            return "Successfully migrated tenant: {}".format(tenant.schema_name)
    except Exception as e:
        # Handle exceptions that may occur during migration.
        return "Error migrating tenant {}: {}".format(tenant.schema_name, e)


class Command(BaseCommand):
    help = "Concurrently migrate tenants"

    def handle(self, *args, **kwargs):
        tenants = get_tenant_model().objects.all()
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit migration jobs for each tenant to the executor.
            future_to_tenant = {
                executor.submit(migrate_tenant, tenant): tenant for tenant in tenants
            }

            for future in as_completed(future_to_tenant):
                tenant = future_to_tenant[future]
                try:
                    data = future.result()
                    self.stdout.write(
                        self.style.SUCCESS(
                            "Successfully migrated {}".format(tenant.name)
                        )
                    )
                except Exception as exc:
                    self.stdout.write(
                        self.style.ERROR(
                            "Error migrating {}: {}".format(tenant.name, exc)
                        )
                    )
