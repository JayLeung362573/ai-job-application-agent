import uuid
from collections.abc import Sequence

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.analysis import Analysis
from app.models.application import Application
from app.schemas.analysis import AnalysisResult
from app.scripts.seed_resume_projects import seed_resume_projects
from app.services.analysis import (
    AnalysisService,
    ApplicationNotFoundError,
    MockAnalysisProvider,
    ResumeProjectContext,
)


def create_test_application(
    db: Session,
    *,
    company: str,
    job_description: str,
) -> Application:
    application = Application(
        company=company,
        title="Software Engineering Intern",
        location="Vancouver, BC",
        job_url="https://example.com/jobs/intern",
        job_description=job_description,
        notes="Analysis service integration test.",
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


def test_analysis_service_saves_structured_result() -> None:
    seed_resume_projects()

    with SessionLocal() as db:
        application = create_test_application(
            db,
            company="Analysis Service Test",
            job_description=(
                "We need Python, FastAPI, and React experience."
            ),
        )

        service = AnalysisService(MockAnalysisProvider())

        analysis = service.analyze_application(
            db=db,
            application_id=application.id,
        )

        assert analysis.id is not None
        assert analysis.application_id == application.id

        assert analysis.required_skills == [
            "Python",
            "FastAPI",
            "React",
        ]
        assert analysis.missing_skills == ["React"]
        assert analysis.match_score == 67

        assert len(analysis.matched_projects) >= 1

        matched_projects_by_name = {
            project["project_name"]: project
            for project in analysis.matched_projects
        }

        assert "Smart Farm IoT Data Pipeline" in matched_projects_by_name

        smart_farm_match = matched_projects_by_name[
            "Smart Farm IoT Data Pipeline"
        ]

        assert smart_farm_match["matched_skills"] == [
            "Python",
            "FastAPI",
        ]

        saved_analysis = db.get(Analysis, analysis.id)

        assert saved_analysis is not None
        assert saved_analysis.match_score == 67
        assert saved_analysis.missing_skills == ["React"]


def test_analysis_service_raises_for_missing_application() -> None:
    service = AnalysisService(MockAnalysisProvider())

    missing_application_id = uuid.UUID(
        "00000000-0000-0000-0000-000000000000"
    )

    with SessionLocal() as db:
        with pytest.raises(
            ApplicationNotFoundError,
            match="was not found",
        ):
            service.analyze_application(
                db=db,
                application_id=missing_application_id,
            )


class FailingAnalysisProvider:
    def analyze(
        self,
        *,
        job_description: str,
        resume_projects: Sequence[ResumeProjectContext],
    ) -> AnalysisResult:
        raise RuntimeError("Provider failed intentionally.")


def test_analysis_service_does_not_save_when_provider_fails() -> None:
    seed_resume_projects()

    with SessionLocal() as db:
        application = create_test_application(
            db,
            company="Provider Failure Test",
            job_description=(
                "We need Python and PostgreSQL experience."
            ),
        )

        count_statement = (
            select(func.count())
            .select_from(Analysis)
            .where(
                Analysis.application_id == application.id
            )
        )

        count_before = db.scalar(count_statement)

        service = AnalysisService(FailingAnalysisProvider())

        with pytest.raises(
            RuntimeError,
            match="Provider failed intentionally",
        ):
            service.analyze_application(
                db=db,
                application_id=application.id,
            )

        count_after = db.scalar(count_statement)

        assert count_before == 0
        assert count_after == 0