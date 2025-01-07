from dental_plan.domains import ITreatmentSelector
from dental_plan.models import PatientTreatment


class PatientTreatmentDataSelector(ITreatmentSelector):
    def get_treatments(self, treatment_ids):
        return PatientTreatment.objects.select_related("treatment").filter(
            id__in=treatment_ids
        )
