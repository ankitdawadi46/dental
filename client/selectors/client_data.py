from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.db.models.functions import ExtractMonth

from client.domains import IClientData
from client.models import Client


class ClientDataSelector(IClientData):
    def get_data(self):
        """
        Retrieves client creation data for the last 8 months.
        Optimized query to aggregate client count by month.
        """
        current_date = datetime.now().date()
        eight_months_ago = current_date - relativedelta(months=8)

        clients_created = (
            Client.objects.filter(
                created_on__gte=eight_months_ago, created_on__lte=current_date
            )
            .annotate(month=ExtractMonth("created_on"))
            .values("month")
            .annotate(count=Count("id"))
        )

        return [
            {"month": item["month"], "count": item["count"]} for item in clients_created
        ]
