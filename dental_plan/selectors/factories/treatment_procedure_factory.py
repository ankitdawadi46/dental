from dental_plan.domains import ITreatmentProcedureFactory
from dental_plan.models import CompanyTreatmentProcedures
from dental_plan.selectors.material_service import MaterialService
from dental_plan.selectors.session_service import SessionService


class TreatmentProcedureFactory(ITreatmentProcedureFactory):
    def __init__(self):
        self.session_manager = SessionService()
        self.material_manager = MaterialService()

    def create(self, validated_data):
        sessions_data = validated_data.pop('company_treatment_procedure_sessions', [])
        materials_data = validated_data.pop('treatment_material_used', [])

        # Create the main procedure
        company_treatment_procedure = CompanyTreatmentProcedures.objects.create(**validated_data)
        
        # Use managers for bulk creation
        if len(sessions_data) > 0:
            self.session_manager.create_sessions(company_treatment_procedure, sessions_data)
        if len(materials_data) > 0:
            self.material_manager.create_materials(company_treatment_procedure, materials_data)

        return company_treatment_procedure

    def update(self, instance, validated_data):
        sessions_data = validated_data.pop('company_treatment_procedure_sessions', [])
        materials_data = validated_data.pop('treatment_material_used', [])

        # Update main procedure
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Use managers for bulk update
        self.session_manager.update_sessions(instance, sessions_data)
        self.material_manager.update_materials(instance, materials_data)

        return instance