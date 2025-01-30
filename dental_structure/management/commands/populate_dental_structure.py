import json
from django.core.management.base import BaseCommand
from dental_structure.models import DentalStructure, Root

class Command(BaseCommand):
    help = "Populate the dental structure and roots based on predefined data"

    def handle(self, *args, **kwargs):
        tooth_data = []

        # Define numbering ranges for each quadrant
        numbering_ranges = {
            "Upper Right": range(11, 19),   # 11-18
            "Upper Left": range(21, 29),    # 21-28
            "Lower Left": range(31, 39),    # 31-38
            "Lower Right": range(41, 49),   # 41-48
        }

        def generate_teeth(quadrant_name, x_offset, y_offset):
            """Generates teeth with appropriate numbering, d3 points, and roots"""
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
            
            teeth = []
            numbering = numbering_ranges[quadrant_name]  # Get the correct numbering sequence
            
            for i, (tooth_type, num_roots) in enumerate(tooth_types):
                tooth_number = numbering[i]  # Assign correct dental numbering
                base_x = x_offset + i * 15

                tooth_data = {
                    "name": f"{quadrant_name} {tooth_type}",
                    "tooth_type": tooth_type,
                    "quadrant": quadrant_name,
                    "num_roots": num_roots,
                    "dental_numbering": tooth_number,  # Assign numbering
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
                            }
                            for j in range(num_roots)
                        ]
                    }
                }
                teeth.append(tooth_data)

            return teeth

        # Generate teeth for each quadrant
        tooth_data.extend(generate_teeth("Upper Right", 10, 10))
        tooth_data.extend(generate_teeth("Upper Left", 110, 10))
        tooth_data.extend(generate_teeth("Lower Left", 110, 50))
        tooth_data.extend(generate_teeth("Lower Right", 10, 50))

        # Insert data into the database
        for tooth in tooth_data:
            dental_structure, created = DentalStructure.objects.get_or_create(
                name=tooth["name"],
                defaults={
                    "tooth_type": tooth["tooth_type"],
                    "quadrant": tooth["quadrant"],
                    "num_roots": tooth["num_roots"],
                    "dental_numbering": tooth["dental_numbering"],
                    "d3_points": json.dumps(tooth["d3_points"]["outline"]),
                },
            )

            # Process and attach roots
            for root in tooth["d3_points"]["roots"]:
                root_obj, root_created = Root.objects.get_or_create(
                    name=root["root_name"],
                    defaults={"d3_points": json.dumps(root["d3_points"])}
                )
                dental_structure.roots.add(root_obj)

        self.stdout.write(self.style.SUCCESS("Dental structure data populated successfully!"))

