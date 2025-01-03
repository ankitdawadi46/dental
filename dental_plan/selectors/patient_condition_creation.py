from dental_plan.domains import IPatientConditionCreation
from dental_plan.models import Condition, PatientCondition

class PatientConditionCreationService(IPatientConditionCreation):
    
    def create_patient_condition(data):
        condition = Condition.objects.get(id=data['condition'])

        return PatientCondition.objects.create(
            name=condition.name,
            description=data.get('condition_description'),
            condition=condition,
            severity=data.get('severity', 'Mild'),
        )