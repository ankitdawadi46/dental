from dental_plan.domains import IDentalHistoryDataFactory
from dental_plan.selectors.condition_selector import PatientConditionDataSelector
from dental_plan.selectors.dental_history_selector import DentalHistorySelector
from dental_plan.selectors.treatment_selector import PatientTreatmentDataSelector


class DentalDataFactory(IDentalHistoryDataFactory):
    @staticmethod
    def get_condition_factory():
        return PatientConditionDataSelector()

    @staticmethod
    def get_treatment_factory():
        return PatientTreatmentDataSelector()

    @staticmethod
    def get_dental_history_factory():
        return DentalHistorySelector()