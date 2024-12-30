# your_app/management/commands/populate_dental_structure.py
import json
from django.core.management.base import BaseCommand
from dental_structure.models import DentalStructure, Root


class Command(BaseCommand):
    help = "Populate the dental structure and roots based on predefined data"

    def handle(self, *args, **kwargs):
        tooth_data = []

        # Generate teeth for each quadrant
        def generate_teeth(start_index, quadrant_name, x_offset, y_offset):
            teeth = []
            tooth_types = [
                ("Central Incisor", 1),
                ("Lateral Incisor", 1),
                ("Canine", 1),
                ("First Premolar", 2),
                ("Second Premolar", 2),
                ("First Molar", 3),
                ("Second Molar", 3),
                ("Third Molar", 3),
            ]
            for i, (tooth_type, num_roots) in enumerate(tooth_types):
                tooth_index = start_index + i
                base_x = x_offset + i * 15
                teeth.append({
                    "name": f"{quadrant_name} {tooth_type}",
                    "tooth_type": tooth_type,
                    "quadrant": quadrant_name,
                    "num_roots": num_roots,
                    "d3_points": {
                        "outline": [
                            [base_x, y_offset],
                            [base_x + 5, y_offset + 5],
                            [base_x, y_offset + 10],
                            [base_x - 5, y_offset + 5]
                        ],
                        "roots": [
                            {
                                "root_name": f"Root {j + 1}",
                                "d3_points": [
                                    [base_x, y_offset + 10],
                                    [base_x + j - (num_roots - 1) / 2, y_offset + 30]
                                ]
                            } for j in range(num_roots)
                        ]
                    }
                })
            return teeth

        # Upper Right Quadrant (1-8)
        tooth_data.extend(generate_teeth(1, "Upper Right", 10, 10))

        # Upper Left Quadrant (9-16)
        tooth_data.extend(generate_teeth(9, "Upper Left", 110, 10))

        # Lower Right Quadrant (17-24)
        tooth_data.extend(generate_teeth(17, "Lower Right", 10, 60))

        # Lower Left Quadrant (25-32)
        tooth_data.extend(generate_teeth(25, "Lower Left", 110, 60))

        # Now, populate the database with the generated tooth data
        for tooth in tooth_data:
            # Create or get the DentalStructure object
            dental_structure, _ = DentalStructure.objects.get_or_create(
                name=tooth["name"],
                defaults={
                    "tooth_type": tooth["tooth_type"],
                    "quadrant": tooth["quadrant"],
                    "num_roots": tooth["num_roots"],
                    "d3_points": json.dumps(tooth["d3_points"]["outline"]),
                },
            )

            # Process and attach roots
            for root in tooth["d3_points"]["roots"]:
                root_obj, root_created = Root.objects.get_or_create(
                    name=root["root_name"],
                    defaults={"d3_points": json.dumps(root["d3_points"])},
                )
                dental_structure.roots.add(root_obj)

        self.stdout.write(self.style.SUCCESS("Dental structure data populated successfully!"))
