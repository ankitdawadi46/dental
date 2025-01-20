from django.core.management.base import BaseCommand
from dental_structure.models import DentalTreatments, DentalTreatmentTypes, DentalTreatmentProcedures

# DENTAL_CONDITION = {
#     'diagnosis': [
#         {'name': "Missing", 'procedures': []},
#         {'name': "Impacted", 'procedures': []},
#         {'name': "Caries", 'procedures':
#             ['stage1/Enamel', 'stage2/Dentine',
#              'stage3/Cementum', 'stage4/Arrested']},
#         {'name': "Pulpitis", 'procedures': []},
#         {'name': "Abscess", 'procedures': []},
#         {'name': "Cracked", 'procedures': []},
#         {'name': "Diastema", 'procedures': []},
#         {'name': "Defect", 'procedures': []},
#         {'name': "Gingiva", 'procedures': []},
#     ],
# }
DENTAL_TREATMENTS = {
    'Aesthetic': [
        {'name': "Cleaning", 'procedures': []},
        {'name': "Fluoride", 'procedures': []},
        {'name': "Sealant", 'procedures': []},
        {'name': "Whitening", 'procedures': []},
    ],
    'Therapy': [
        {'name': "Restoration", 'procedures': [
            'Permanent', 'Temporary', 'Amalgam',
            'Glass Ionomer']},
        {'name': "Root Canal", 'procedures': [
            'Permanent', 'temporary', 'Calcium',
            'Gutta Percha']},
        {'name': "Post and Core", 'procedures': []},
    ],
    'Prosthodontics': [
        {'name': "Veneer", 'procedures': []},
        {'name': "Onlay", 'procedures': []},
        {'name': "Crown", 'procedures': [
            'Permanent',
            'Temporary',
            'Gold',
            'Zirconia']},
       {'name': 'Denture', 'procedures': []},
       {'name': 'Bridge', 'procedures': []}],
    'Surgery': [
        {'name': "Extraction", 'procedures': []},
        {'name': "Implant", 'procedures': []},
        {'name': "Bone Rafting", 'procedures': []},
        {'name': "Resection", 'procedures': []},]
}

class Command(BaseCommand):
    help = "Populates DentalTreatments, DentalTreatmentTypes, and DentalTreatmentProcedures models"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to populate dental data...")

        for treatment_name, treatment_types in DENTAL_TREATMENTS.items():
            # Create or get the DentalTreatment instance
            dental_treatment, created = DentalTreatments.objects.get_or_create(
                service_name=treatment_name,
                defaults={"service_description": f"{treatment_name} description"}
            )
            if created:
                self.stdout.write(f"Created DentalTreatment: {treatment_name}")

            for treatment_type in treatment_types:
                # Create or get the DentalTreatmentType instance
                dental_treatment_type, created = DentalTreatmentTypes.objects.get_or_create(
                    service_name=dental_treatment,
                    service_type_name=treatment_type['name'],
                    defaults={"service_description": f"{treatment_type['name']} description"}
                )
                if created:
                    self.stdout.write(f"  Created DentalTreatmentType: {treatment_type['name']}")

                for procedure_name in treatment_type['procedures']:
                    # Create or get the DentalTreatmentProcedure instance
                    procedure, created = DentalTreatmentProcedures.objects.get_or_create(
                        procedure_name=procedure_name,
                        dental_service_type=dental_treatment_type
                    )
                    if created:
                        self.stdout.write(f"    Created DentalTreatmentProcedure: {procedure_name}")

        self.stdout.write(self.style.SUCCESS("Successfully populated dental data."))