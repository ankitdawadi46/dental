from client.domains import (
    ICardDetails,
    IClientData,
    IDashboardDataFactory,
    IPaymentPending,
)
from client.selectors.card_detail import CardDetailsSelector
from client.selectors.client_data import ClientDataSelector
from client.selectors.payment_pending import PaymentPendingSelector


class DashboardDataFactory(IDashboardDataFactory):
    def __init__(
        self,
        card_details_selector=None,
        payment_pending_selector=None,
        client_data_selector=None,
    ):
        """
        Constructor that allows injecting custom selectors for flexibility.
        """
        self.card_details_selector = card_details_selector or CardDetailsSelector()
        self.payment_pending_selector = (
            payment_pending_selector or PaymentPendingSelector()
        )
        self.client_data_selector = client_data_selector or ClientDataSelector()

    def get_card_details(self) -> ICardDetails:
        return self.card_details_selector.get_data()

    def get_payment_pending(self) -> IPaymentPending:
        return self.payment_pending_selector.get_data()

    def get_client_data(self) -> IClientData:
        return self.client_data_selector.get_data()
