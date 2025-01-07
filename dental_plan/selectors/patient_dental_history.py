
from dental_plan.domains import IPatientDentalHistoryCreation
from dental_plan.models import DentalHistory
from dental_structure.models import DentalStructure


class DentalHistoryService(IPatientDentalHistoryCreation):
    def create_dental_history(data, patient_condition, patient_treatment):
        dental_structure = DentalStructure.objects.get(id=data['dental_structure'])

        return DentalHistory.objects.create(
            patient_id=data['patient'],
            dental_structure=dental_structure,
            date=data['date'],
            condition=patient_condition,
            treatment=patient_treatment,
            notes=data.get('notes', '')
        )