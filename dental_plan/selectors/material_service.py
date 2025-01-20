from dental_plan.domains import IMaterialService
from dental_plan.models import TreatmentMaterialUsed


class MaterialService(IMaterialService):
    def create_materials(self, company_treatment_procedure, materials_data):
        # Prepare a list of objects to be created in bulk
        material_objects = [
            TreatmentMaterialUsed(
                patient_treatment=company_treatment_procedure, **material_data
            )
            for material_data in materials_data
        ]
        # Perform bulk create
        TreatmentMaterialUsed.objects.bulk_create(material_objects)

    def update_materials(self, company_treatment_procedure, materials_data):
        # Delete existing materials and recreate them
        company_treatment_procedure.treatment_material_used.all().delete()
        if len(materials_data) > 0:
            self.create_materials(company_treatment_procedure, materials_data)
