from django.db import transaction

from dental_plan.domains import IPatientDentalHistoryFactory
from dental_plan.selectors.patient_condition_creation import PatientConditionCreationService
from dental_plan.selectors.patient_dental_history import DentalHistoryService
from dental_plan.selectors.patient_treatment_creation import PatientTreatmentCreationService

class DentalHistoryFactory(IPatientDentalHistoryFactory):
    @transaction.atomic
    def create_full_dental_history(data):
        patient_condition = PatientConditionCreationService.create_patient_condition(data)
        patient_treatment = PatientTreatmentCreationService.create_patient_treatment(data)
        dental_history = DentalHistoryService.create_dental_history(data)

        return {
            "dental_history": dental_history,
            "patient_condition": patient_condition,
            "patient_treatment": patient_treatment
        }