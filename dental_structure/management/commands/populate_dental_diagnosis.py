from django.core.management.base import BaseCommand
from dental_structure.models import DentalDiagnosis, DentalDiagnosisTypes, DentalDiagnosisProcedures

# DENTAL_CONDITION dictionary
DENTAL_CONDITION = {
    'diagnosis': [
        {'name': "Missing", 'procedures': []},
        {'name': "Impacted", 'procedures': []},
        {'name': "Caries", 'procedures': [
            'stage1/Enamel', 'stage2/Dentine',
            'stage3/Cementum', 'stage4/Arrested']},
        {'name': "Pulpitis", 'procedures': []},
        {'name': "Abscess", 'procedures': []},
        {'name': "Cracked", 'procedures': []},
        {'name': "Diastema", 'procedures': []},
        {'name': "Defect", 'procedures': []},
        {'name': "Gingiva", 'procedures': []},
    ],
}

class Command(BaseCommand):
    help = "Populates DentalDiagnosis, DentalDiagnosisTypes, and DentalDiagnosisProcedures models"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to populate dental condition data...")

        for diagnosis_name, diagnosis_types in DENTAL_CONDITION.items():
            # Create or get the DentalDiagnosis instance
            dental_diagnosis, created = DentalDiagnosis.objects.get_or_create(
                service_name=diagnosis_name,
                defaults={"service_description": f"{diagnosis_name} description"}
            )
            if created:
                self.stdout.write(f"Created DentalDiagnosis: {diagnosis_name}")

            for diagnosis_type in diagnosis_types:
                # Create or get the DentalDiagnosisType instance
                dental_diagnosis_type, created = DentalDiagnosisTypes.objects.get_or_create(
                    service_name=dental_diagnosis,
                    service_type_name=diagnosis_type['name'],
                    defaults={"service_description": f"{diagnosis_type['name']} description"}
                )
                if created:
                    self.stdout.write(f"  Created DentalDiagnosisType: {diagnosis_type['name']}")

                for procedure_name in diagnosis_type['procedures']:
                    # Create or get the DentalDiagnosisProcedure instance
                    procedure, created = DentalDiagnosisProcedures.objects.get_or_create(
                        procedure_name=procedure_name,
                        dental_service_type=dental_diagnosis_type
                    )
                    if created:
                        self.stdout.write(f"    Created DentalDiagnosisProcedure: {procedure_name}")

        self.stdout.write(self.style.SUCCESS("Successfully populated dental condition data."))
