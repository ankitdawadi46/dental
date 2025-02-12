from abc import ABC, abstractmethod
from typing import Dict

from django.contrib.auth import get_user_model

from client.models import Client

User = get_user_model()


class ICardDetails(ABC):
    @abstractmethod
    def get_data(self):
        """
        Abstract method to retrieve the card details data.
        """
        pass


class IPaymentPending(ABC):
    @abstractmethod
    def get_data(self):
        """
        Abstract method to retrieve the payment pending client data.
        """
        pass


class IClientData(ABC):
    @abstractmethod
    def get_data(self):
        """
        Abstract method to retrieve the client data for the last 8 months.
        """
        pass


class IDashboardDataFactory(ABC):
    @abstractmethod
    def get_card_details(self) -> ICardDetails:
        pass

    @abstractmethod
    def get_payment_pending(self) -> IPaymentPending:
        pass

    @abstractmethod
    def get_client_data(self) -> IClientData:
        pass


class ICreateClient(ABC):
    @abstractmethod
    def create_client(self, data: Dict) -> Client:
        pass


class ISetupDomain(ABC):
    @abstractmethod
    def setup_domain(self, client: Client):
        pass


class ISetupDNS(ABC):
    @abstractmethod
    def setup_dns(self, client: Client):
        pass


class ICreateClientUser(ABC):
    @abstractmethod
    def create_user(self, client: Client, password: str) -> User:
        pass
    

class IUserService(ABC):
    @abstractmethod
    def validate_profile_type(self, data):
        pass

    @abstractmethod
    def get_or_create_user(self, user_data):
        pass
    
    @abstractmethod
    def update_user(self, user, user_data):
        pass

class IProfileService(ABC):
    @abstractmethod
    def create_profile(self, profile_data):
        pass

    @abstractmethod
    def update_profile(self, profile, profile_data):
        pass

class IClinicProfileService(ABC):
    @abstractmethod
    def handle_clinic_profile(self, profile, clinic_data):
        pass


class IClientCreationFactory(ABC):
    @abstractmethod
    def create_client_with_dns_and_user(self, client_data: Dict) -> Client:
        pass


class IClientSupportUserFactory(ABC):
    @abstractmethod
    def create_support_user(self, client_data: Dict) -> Client:
        pass
