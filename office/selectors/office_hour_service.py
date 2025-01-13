from office.models import OfficeHours

class OfficeHoursService:
    @staticmethod
    def create_bulk_office_hours(validated_data):
        """
        Handles the creation of multiple OfficeHours records.
        :param validated_data: Validated data from the serializer.
        :return: None
        """
        office_hours_objects = []

        for entry in validated_data:
            employee_id = entry["employee_id"]
            for day_data in entry["days"]:
                for time_slot in day_data["time_slots"]:
                    office_hours_objects.append(
                        OfficeHours(
                            day=day_data["day"],
                            is_active=day_data["is_active"],
                            start_time=time_slot["start_time"],
                            end_time=time_slot["end_time"],
                            employee_id=employee_id,
                        )
                    )

        # Bulk create OfficeHours
        OfficeHours.objects.bulk_create(office_hours_objects)
