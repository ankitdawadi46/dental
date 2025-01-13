from abc import ABC, abstractmethod


class IPatientConditionCreation(ABC):
    @abstractmethod
    def create_patient_condition(self):
        pass


class IPatientTreatmentCreation(ABC):
    @abstractmethod
    def create_patient_treatment(self):
        pass


class IPatientDentalHistoryCreation(ABC):
    @abstractmethod
    def create_dental_history(self):
        pass


class IDentalHistorySelector(ABC):
    @abstractmethod
    def dental_history_data(self):
        pass


class IConditionSelector(ABC):
    @abstractmethod
    def get_conditions(self):
        pass


class ITreatmentSelector(ABC):
    @abstractmethod
    def get_treatments(self):
        pass


class IPatientDentalHistoryFactory(ABC):
    @abstractmethod
    def create_full_dental_history(self):
        pass


class IDentalHistoryDataFactory(ABC):
    @abstractmethod
    def get_condition_factory():
        pass

    @abstractmethod
    def get_treatment_factory():
        pass

    @abstractmethod
    def get_dental_history_factory():
        pass
    

class IPaymentSelector(ABC):
    @abstractmethod
    def get_payments(self):
        pass
