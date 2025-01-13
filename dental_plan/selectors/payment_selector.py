from dental_plan.domains import IPaymentSelector
from dental_plan.models import Payment


class PatientPaymentDataSelector(IPaymentSelector):
    def get_payments(self, treatment_ids):
        return Payment.objects.select_related('patient_treatment').filter(
            patient_treatment_id__in=treatment_ids
        )