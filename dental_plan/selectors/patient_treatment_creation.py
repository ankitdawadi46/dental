from dental_plan.domains import IPatientTreatmentCreation
from dental_plan.models import PatientTreatment, Treatment


class PatientTreatmentCreationService(IPatientTreatmentCreation):
    
    def create_patient_treatment(data):
        treatment = Treatment.objects.get(id=data['treatment'])

        return PatientTreatment.objects.create(
            name=treatment.name,
            description=data.get('treatment_description'),
            material_used=data.get('material_used', ''),
            d3_image=data.get('treatment_d3_image', {})
        )