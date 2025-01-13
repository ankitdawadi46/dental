from django.db import connection
from dental_plan.domains import IDentalHistorySelector
from dental_plan.models import DentalHistory, PatientCondition, PatientTreatment
from django.db.models import Prefetch


class DentalHistorySelector(IDentalHistorySelector):
    def dental_history_data(self, patient_id, dental_structure_id):
        data =  (
            DentalHistory.objects.filter(
                patient_id=patient_id, dental_structure_id=dental_structure_id
            )
            .select_related("condition", "dental_structure", "treatment")
            # .prefetch_related(
            #     Prefetch(
            #         "condition__condition",
            #         queryset=PatientCondition.objects.select_related("condition"),
            #     ),
            #     Prefetch(
            #         "treatment__treatment",
            #         queryset=PatientTreatment.objects.select_related("treatment"),
            #     ),
            # )
        )
        return data