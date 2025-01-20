from dental_structure.models import DentalTreatments


class DentalTreatmentFactory:
    @staticmethod
    def get_flattened_dental_treatments():
        """
        Fetches dental treatments and returns a flattened list.
        """
        flattened_data = []

        treatments = DentalTreatments.objects.prefetch_related(
            'dentaltreatmenttypes_set__dentaltreatmentprocedures_set'
        )

        for treatment in treatments:
            service_name = treatment.service_name

            for treatment_type in treatment.dentaltreatmenttypes_set.all():
                service_type_name = treatment_type.service_type_name

                procedures = treatment_type.dentaltreatmentprocedures_set.all()
                if procedures.exists():
                    for procedure in procedures:
                        # Add treatment, type, and procedure
                        flattened_data.append(
                           {'procedure_id': procedure.id, 'procedure_name': f"{service_name}-{service_type_name}-{procedure.procedure_name}", 'depth': 2}
                        )
                else:
                    # Add treatment and type only
                    flattened_data.append(
                        {'service_type_id': treatment_type.id, 'service_type_name': f"{service_name}-{service_type_name}", 'depth': 1})

        return flattened_data