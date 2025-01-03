from dental_plan.domains import IConditionSelector
from dental_plan.models import PatientCondition


class PatientConditionDataSelector(IConditionSelector):
    def get_conditions(self, condition_ids):
        return PatientCondition.objects.select_related("condition").filter(
            condition_id__in=condition_ids
        )
