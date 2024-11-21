# from datetime import timezone

# from dateutil.relativedelta import relativedelta
# from django.db.models import Count
# from django.db.models.functions import ExtractMonth

# from client.domains import (
#     ICardDetailsSelectorInterface,
#     IClientDataInterface,
#     IClientDataSelectorInterface,
#     IPaymentPendingSelectorInterface,
# )
# from client.models import Client


# class CardDetailsSelector(ICardDetailsSelectorInterface):
#     def get_data(self):
#         """
#         Retrieves total clients, active clients, and trial clients.
#         Uses optimized queries.
#         """
#         total_clients = Client.objects.count()
#         active_clients = Client.objects.filter(is_enabled=True).count()
#         trial_clients = Client.objects.filter(is_trial=True).count()

#         return {
#             "total_clients": total_clients,
#             "active_clients": active_clients,
#             "trial_clients": trial_clients,
#         }


# class PaymentPendingSelector(IPaymentPendingSelectorInterface):
#     def get_data(self):
#         """
#         Retrieves clients with pending payments.
#         Filters clients whose `paid_until` is in the past and `paid_until` is not null.
#         """
#         today = timezone.now().date()
#         clients = Client.objects.filter(
#             paid_until__isnull=False, paid_until__date__lte=today
#         )[:6]
#         return [{"id": client.id, "name": client.name} for client in clients]


# class ClientDataSelector(IClientDataSelectorInterface):
#     def get_data(self):
#         """
#         Retrieves client creation data for the last 8 months.
#         Optimized query to aggregate client count by month.
#         """
#         current_date = timezone.now().date()
#         eight_months_ago = current_date - relativedelta(months=8)

#         clients_created = (
#             Client.objects.filter(
#                 created_on__gte=eight_months_ago, created_on__lte=current_date
#             )
#             .annotate(month=ExtractMonth("created_on"))
#             .values("month")
#             .annotate(count=Count("id"))
#         )

#         return [
#             {"month": item["month"], "count": item["count"]} for item in clients_created
#         ]


# class DefaultClientDataSelector(IClientDataInterface):
#     def __init__(
#         self,
#         card_details_selector=None,
#         payment_pending_selector=None,
#         client_data_selector=None,
#     ):
#         """
#         Constructor that allows injecting custom selectors for flexibility.
#         """
#         self.card_details_selector = card_details_selector or CardDetailsSelector()
#         self.payment_pending_selector = (
#             payment_pending_selector or PaymentPendingSelector()
#         )
#         self.client_data_selector = client_data_selector or ClientDataSelector()

#     def get_card_details(self) -> ICardDetailsSelectorInterface:
#         return self.card_details_selector

#     def get_payment_pending(self) -> IPaymentPendingSelectorInterface:
#         return self.payment_pending_selector

#     def get_client_data(self) -> IClientDataSelectorInterface:
#         return self.client_data_selector
