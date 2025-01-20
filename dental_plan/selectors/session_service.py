from dental_plan.domains import ISessionService
from dental_plan.models import CompanyTreamentProcedureSession


class SessionService(ISessionService):
    
    def create_sessions(self, company_treatment_procedure, sessions_data):
        # Prepare a list of objects to be created in bulk
        session_objects = [
            CompanyTreamentProcedureSession(
                company_treatment_procedures=company_treatment_procedure, 
                **session_data
            )
            for session_data in sessions_data
        ]
        # Perform bulk create
        CompanyTreamentProcedureSession.objects.bulk_create(session_objects)
        
    def update_sessions(self, company_treatment_procedure, sessions_data):
        # Delete existing sessions and recreate them
        company_treatment_procedure.company_treatment_procedure_sessions.all().delete()
        if len(sessions_data) > 0:
            self.create_sessions(company_treatment_procedure, sessions_data)