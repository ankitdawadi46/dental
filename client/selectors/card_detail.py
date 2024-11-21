from client.domains import ICardDetails
from client.models import Client


class CardDetailsSelector(ICardDetails):
    def get_data(self):
        """
        Retrieves total clients, active clients, and trial clients.
        Uses optimized queries.
        """
        total_clients = Client.objects.count()
        active_clients = Client.objects.filter(is_enabled=True).count()
        trial_clients = Client.objects.filter(on_trial=True).count()

        return {
            "total_clients": total_clients,
            "active_clients": active_clients,
            "trial_clients": trial_clients,
        }
