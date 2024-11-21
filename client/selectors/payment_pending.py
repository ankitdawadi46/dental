from datetime import datetime
from client.domains import IPaymentPending
from client.models import Client


class PaymentPendingSelector(IPaymentPending):
    def get_data(self):
        """
        Retrieves clients with pending payments.
        Filters clients whose `paid_until` is in the past and `paid_until` is not null.
        """
        today = datetime.now().date()
        clients = Client.objects.filter(
            paid_until__isnull=False, paid_until__date__lte=today
        )[:6]
        return [{"id": client.id, "name": client.name} for client in clients]