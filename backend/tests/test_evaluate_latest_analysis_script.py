import uuid

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.analysis import Analysis
from app.models.application import Application
from app.scripts.evaluate_latest_analysis import (
    EvaluationTargetNotFoundError,
    build_analysis_result_from_model,
    evaluate_saved_analysis,
    format_evaluation_report,
    load_latest_analysis,
    main,
)
from app.scripts.seed_resume_projects import seed_resume_projects
from app.services.analysis import (
    AnalysisEvaluationIssue,
    AnalysisEvaluationReport,
)


def create_application_with_analysis(
    db: Session,
) -> tuple[Application, Analysis]:
    application = Application(
        company="Evaluation Script Test",
        title="Software Engineering Intern",
        location="Vancouver, BC",
        job_url="https://example.com/jobs/evaluation-script-test",
        job_description=(
            "We need Python, FastAPI, PostgreSQL, Docker, "
            "and React experience."
        ),
        notes="Evaluation script integration test.",
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    analysis = Analysis(
        application_id=application.id,
        required_skills=[
            "Python",
            "FastAPI",
            "React",
        ],
        preferred_skills=[
            "Docker",
        ],
        responsibilities=[
            "Build and maintain backend APIs.",
        ],
        matched_projects=[
            {
                "project_name": "Smart Farm IoT Data Pipeline",
                "matched_skills": [
                    "Python",
                    "FastAPI",
                    "Docker",
                ],
                "reason": (
                    "The project demonstrates backend API work "
                    "with FastAPI."
                ),
            }
        ],
        missing_skills=[
            "React",
        ],
        suggested_bullets=[
            {
                "project_name": "Smart Farm IoT Data Pipeline",
                "bullet": (
                    "Built a containerized FastAPI telemetry service "
                    "backed by PostgreSQL."
                ),
                "target_skill": "FastAPI",
            }
        ],
        interview_questions=[
            (
                "How did you design the FastAPI service in the "
                "Smart Farm IoT Data Pipeline project?"
            ),
        ],
        match_score=75,
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return application, analysis


def test_build_analysis_result_from_model() -> None:
    analysis = Analysis(
        application_id=uuid.uuid4(),
        required_skills=[
            "Python",
        ],
        preferred_skills=[],
        responsibilities=[
            "Build APIs.",
        ],
        matched_projects=[
            {
                "project_name": "Smart Farm IoT Data Pipeline",
                "matched_skills": [
                    "Python",
                ],
                "reason": "Uses Python.",
            }
        ],
        missing_skills=[
            "React",
        ],
        suggested_bullets=[
            {
                "project_name": "Smart Farm IoT Data Pipeline",
                "bullet": (
                    "Built a Python telemetry service for sensor data."
                ),
                "target_skill": "Python",
            }
        ],
        interview_questions=[
            "How did you use Python in the project?",
        ],
        match_score=50,
    )

    result = build_analysis_result_from_model(analysis)

    assert result.required_skills == ["Python"]
    assert result.matched_projects[0].project_name == (
        "Smart Farm IoT Data Pipeline"
    )
    assert result.match_score == 50


def test_format_evaluation_report_for_passed_result() -> None:
    report = AnalysisEvaluationReport(
        issues=(),
        warnings=(),
    )

    output = format_evaluation_report(report)

    assert "Analysis evaluation: PASSED" in output
    assert "Issues: 0" in output
    assert "Warnings: 0" in output


def test_format_evaluation_report_includes_issues_and_warnings() -> None:
    report = AnalysisEvaluationReport(
        issues=(
            AnalysisEvaluationIssue(
                code="unknown_matched_project",
                message="Matched project does not exist.",
            ),
        ),
        warnings=(
            AnalysisEvaluationIssue(
                code="short_suggested_bullet",
                message="Suggested bullet is too short.",
            ),
        ),
    )

    output = format_evaluation_report(report)

    assert "Analysis evaluation: FAILED" in output
    assert "[unknown_matched_project]" in output
    assert "Matched project does not exist." in output
    assert "[short_suggested_bullet]" in output
    assert "Suggested bullet is too short." in output


def test_load_latest_analysis_raises_for_missing_application() -> None:
    with SessionLocal() as db:
        missing_application_id = uuid.UUID(
            "00000000-0000-0000-0000-000000000000"
        )

        try:
            load_latest_analysis(
                db,
                application_id=missing_application_id,
            )
        except EvaluationTargetNotFoundError as exc:
            assert "was not found" in str(exc)
        else:
            raise AssertionError(
                "Expected EvaluationTargetNotFoundError."
            )


def test_evaluate_saved_analysis_passes_for_grounded_result() -> None:
    seed_resume_projects()

    with SessionLocal() as db:
        application, _analysis = create_application_with_analysis(db)

        report = evaluate_saved_analysis(
            db=db,
            application_id=application.id,
        )

        assert report.passed is True
        assert report.issues == ()


def test_main_rejects_invalid_uuid(capsys) -> None:
    exit_code = main(["not-a-valid-uuid"])

    captured = capsys.readouterr()

    assert exit_code == 2
    assert "application_id must be a valid UUID" in captured.err