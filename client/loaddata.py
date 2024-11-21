import os
# import json
# import requests

# from datetime import datetime

from django.contrib.auth.models import Group, Permission
# from django.conf import settings

# from company.models import OfficeHoliday, OfficeHours

# from system.models import Services, ServiceCategory


# def save_permissions_to_file(group_name, folder_path="external_files/permission_lists"):
#     filename = f"{group_name.lower()}_permissions.txt"
#     filepath = os.path.join(folder_path, filename)
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)
#     with open(filepath, "w") as f:
#         group = Group.objects.get(name=group_name)
#         for permission in group.permissions.all():
#             f.write(f"{permission.content_type.app_label}.{permission.codename}\n")


# def load_groups_permission():
#     g_list = ["SuperAdmin", "Admin", "Professional", "Client"]
#     for group_name in g_list:
#         save_permissions_to_file(group_name)


def populate_permissions_from_files(folder_path="external_files/permission_lists"):
    group_names = ["SuperAdmin", "Admin", "Professional", "Client"]
    for group_name in group_names:
        filename = f"{group_name.lower()}_permissions.txt"
        filepath = os.path.join(folder_path, filename)
        with open(filepath, "r") as f:
            group, _ = Group.objects.get_or_create(name=group_name)
            for line in f:
                app_label, codename = line.strip().split(".")
                permission = Permission.objects.get(
                    content_type__app_label=app_label, codename=codename
                )
                # Check if permission already exists for the group
                if not group.permissions.filter(id=permission.id).exists():
                    group.permissions.add(permission)


# def get_current_nepali_year():
#     return 2080


# def create_english_holidays(english_year=2024):
#     response = requests.get(
#         f"https://date.nager.at/api/v3/PublicHolidays/{english_year}/AT"
#     )
#     if response.status_code == 200:
#         holidays = response.json()
#         for holiday in holidays:
#             name = holiday.get("name", None)
#             date_str = holiday.get("date", None)
#             holiday_date = datetime.strptime(date_str, "%Y-%m-%d").date()
#             if not OfficeHoliday.objects.filter(
#                 name=name, holiday_date=holiday_date
#             ).exists():
#                 OfficeHoliday.objects.create(name=name, holiday_date=holiday_date)
#                 # print(f'Successfully added holiday "{name}" on {holiday_date}.')
#                 # print('Finished populating public holidays.')


# def populate_public_holidays(calendar_type, nepali_year=None):
#     OfficeHoliday.objects.all().delete()
#     # print(calendar_type)
#     if calendar_type == "english":
#         create_english_holidays()
#         return

#     if nepali_year is None:
#         nepali_year = get_current_nepali_year()
#     file_path = (
#         f"{settings.BASE_DIR}/external_files/holidays/artifact-{nepali_year}.json"
#     )
#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             holidays_data = json.load(file)
#     except FileNotFoundError:
#         # print(f'The file for the Nepali year {nepali_year} does not exist.')
#         return

#     for date_str, details in holidays_data.items():
#         if details.get("is_public_holiday", True):
#             holiday_date = datetime.strptime(date_str, "%Y/%m/%d").date()
#             event = details.get("events", [])[0]
#             if not OfficeHoliday.objects.filter(
#                 name=event, holiday_date=holiday_date
#             ).exists():
#                 OfficeHoliday.objects.create(name=event, holiday_date=holiday_date)
#                 # print(f'Successfully added holiday "{event}" on {holiday_date}.')
#             else:
#                 # print(f'Holiday "{event}" on {holiday_date} already exists in the database.')
#                 pass
#     # print('Finished populating public holidays.')


# def populate_services_from_json(service_file):
#     # print(service_file)
#     try:
#         decoded_file = service_file.read().decode("utf-8")
#         data_list = json.loads(decoded_file)

#         for data in data_list:
#             category_data = data.get("catg_name")
#             if not category_data:
#                 return False
#             category, created = ServiceCategory.objects.get_or_create(
#                 name=category_data
#             )
#             services_data = data.get("services", [])
#             if not isinstance(services_data, list):
#                 return False

#             for service_data in services_data:
#                 # print(service_data,900000000000000000000000000)
#                 name = service_data.get("name")
#                 color_hex = service_data.get("color_hex")
#                 short_description = service_data.get("short_description")
#                 duration = service_data.get("duration")
#                 default_price = service_data.get("default_price")
#                 priority = service_data.get("priority")
#                 is_active = service_data.get("is_active")

#                 # Create or update service
#                 service, created = Services.objects.update_or_create(
#                     name=name,
#                     defaults={
#                         "category": category,
#                         "color_hex": color_hex,
#                         "short_description": short_description,
#                         "duration": duration,
#                         "default_price": default_price,
#                         "priority": priority,
#                         "is_active": is_active,
#                     },
#                 )

#     except Exception as e:
#         return False

#     return True


# def populate_office_hrs(start_time, end_time):
#     DAY_CHOICES = [
#         (1, "Sunday"),
#         (2, "Monday"),
#         (3, "Tuesday"),
#         (4, "Wednesday"),
#         (5, "Thursday"),
#         (6, "Friday"),
#         (0, "Saturday"),
#     ]

#     def is_weekend(day):
#         return day in [0, 1]  # Saturday or Sunday

#     for day, _ in DAY_CHOICES:
#         is_active = not is_weekend(day)
#         office_hour, created = OfficeHours.objects.get_or_create(day=day)
#         office_hour.start_time = start_time
#         office_hour.end_time = end_time
#         office_hour.is_active = is_active
#         office_hour.save()
