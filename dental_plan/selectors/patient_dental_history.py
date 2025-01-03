
from dental_plan.domains import IPatientDentalHistoryCreation
from dental_plan.models import DentalHistory
from dental_structure.models import DentalStructure


class DentalHistoryService(IPatientDentalHistoryCreation):
    def create_dental_history(data):
        dental_structure = DentalStructure.objects.get(id=data['dental_structure'])

        return DentalHistory.objects.create(
            patient_id=data['patient'],
            dental_structure=dental_structure,
            date=data['date'],
            condition_id=data['condition'],
            treatment_id=data['treatment'],
            notes=data.get('notes', '')
        )