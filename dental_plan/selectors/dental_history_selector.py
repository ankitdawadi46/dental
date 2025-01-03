from dental_plan.domains import IDentalHistorySelector
from dental_plan.models import DentalHistory, PatientCondition, PatientTreatment
from django.db.models import Prefetch


class DentalHistorySelector(IDentalHistorySelector):
    def dental_history_data(self, patient_id, dental_structure_id):
        return (
            DentalHistory.objects.filter(
                patient_id=patient_id, dental_structure_id=dental_structure_id
            )
            # Use select_related for ForeignKey and OneToOne relations
            .select_related("condition", "dental_structure")
            # Use prefetch_related for ManyToMany and reverse ForeignKey relations
            .prefetch_related(
                Prefetch(
                    "condition__patientcondition_set",
                    queryset=PatientCondition.objects.select_related("condition"),
                ),
                Prefetch(
                    "treatment__patienttreatment_set",  # Reverse relation or ManyToMany relation
                    queryset=PatientTreatment.objects.select_related("treatment"),
                ),
            )
        )