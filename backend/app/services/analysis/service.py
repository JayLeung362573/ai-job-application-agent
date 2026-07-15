import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.models.application import Application
from app.models.resume_project import ResumeProject
from app.services.analysis.provider import (
    AnalysisProvider,
    ResumeProjectContext,
)


class ApplicationNotFoundError(LookupError):
    """Raised when an application cannot be found for analysis."""


class AnalysisService:
    def __init__(self, provider: AnalysisProvider) -> None:
        self.provider = provider

    def analyze_application(
        self,
        *,
        db: Session,
        application_id: uuid.UUID,
    ) -> Analysis:
        application = db.get(Application, application_id)

        if application is None:
            raise ApplicationNotFoundError(
                f"Application {application_id} was not found."
            )

        statement = select(ResumeProject).order_by(
            ResumeProject.name
        )
        resume_projects = db.scalars(statement).all()

        project_contexts = [
            ResumeProjectContext(
                name=project.name,
                tech_stack=tuple(project.tech_stack),
                description=project.description,
                resume_bullets=tuple(project.resume_bullets),
            )
            for project in resume_projects
        ]

        result = self.provider.analyze(
            job_description=application.job_description,
            resume_projects=project_contexts,
        )

        result_data = result.model_dump(mode="json")

        analysis = Analysis(
            application_id=application.id,
            required_skills=result_data["required_skills"],
            preferred_skills=result_data["preferred_skills"],
            responsibilities=result_data["responsibilities"],
            matched_projects=result_data["matched_projects"],
            missing_skills=result_data["missing_skills"],
            suggested_bullets=result_data["suggested_bullets"],
            interview_questions=result_data[
                "interview_questions"
            ],
            match_score=result_data["match_score"],
        )

        try:
            db.add(analysis)
            db.commit()
            db.refresh(analysis)
        except Exception:
            db.rollback()
            raise

        return analysis