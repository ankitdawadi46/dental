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

    
class ISessionService(ABC):
    @abstractmethod
    def create_sessions(self):
        pass
    
    @abstractmethod
    def update_sessions(self):
        pass
    

class IMaterialService(ABC):
    @abstractmethod
    def create_materials(self):
        pass
    
    @abstractmethod
    def update_materials(self):
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
    

class ITreatmentProcedureFactory(ABC):
    @abstractmethod
    def create(self, validated_data):
        """Abstract method for creating an entity."""
        pass

    @abstractmethod
    def update(self, instance, validated_data):
        """Abstract method for updating an entity."""
        pass
    

class IPaymentSelector(ABC):
    @abstractmethod
    def get_payments(self):
        pass
