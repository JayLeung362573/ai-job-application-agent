import argparse
import sys
import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.analysis import Analysis
from app.models.application import Application
from app.models.resume_project import ResumeProject
from app.schemas.analysis import AnalysisResult
from app.services.analysis import (
    AnalysisEvaluationReport,
    ResumeProjectContext,
    evaluate_analysis_result,
)


class EvaluationTargetNotFoundError(LookupError):
    """Raised when the evaluation target cannot be found."""


def load_latest_analysis(
    db: Session,
    *,
    application_id: uuid.UUID,
) -> Analysis:
    application = db.get(Application, application_id)

    if application is None:
        raise EvaluationTargetNotFoundError(
            f"Application {application_id} was not found."
        )

    statement = (
        select(Analysis)
        .where(Analysis.application_id == application_id)
        .order_by(
            Analysis.created_at.desc(),
            Analysis.id.desc(),
        )
        .limit(1)
    )

    analysis = db.scalar(statement)

    if analysis is None:
        raise EvaluationTargetNotFoundError(
            f"Application {application_id} has no saved analysis."
        )

    return analysis


def load_resume_project_contexts(
    db: Session,
) -> tuple[ResumeProjectContext, ...]:
    statement = select(ResumeProject).order_by(ResumeProject.name)

    resume_projects = db.scalars(statement).all()

    return tuple(
        ResumeProjectContext(
            name=project.name,
            tech_stack=tuple(project.tech_stack),
            description=project.description,
            resume_bullets=tuple(project.resume_bullets),
        )
        for project in resume_projects
    )


def build_analysis_result_from_model(
    analysis: Analysis,
) -> AnalysisResult:
    return AnalysisResult(
        required_skills=list(analysis.required_skills),
        preferred_skills=list(analysis.preferred_skills),
        responsibilities=list(analysis.responsibilities),
        matched_projects=list(analysis.matched_projects),
        missing_skills=list(analysis.missing_skills),
        suggested_bullets=list(analysis.suggested_bullets),
        interview_questions=list(analysis.interview_questions),
        match_score=analysis.match_score,
    )


def evaluate_saved_analysis(
    *,
    db: Session,
    application_id: uuid.UUID,
) -> AnalysisEvaluationReport:
    analysis = load_latest_analysis(
        db,
        application_id=application_id,
    )

    result = build_analysis_result_from_model(analysis)
    resume_projects = load_resume_project_contexts(db)

    return evaluate_analysis_result(
        result=result,
        resume_projects=resume_projects,
    )


def format_evaluation_report(
    report: AnalysisEvaluationReport,
) -> str:
    status = "PASSED" if report.passed else "FAILED"

    lines = [
        f"Analysis evaluation: {status}",
        f"Issues: {len(report.issues)}",
        f"Warnings: {len(report.warnings)}",
    ]

    if report.issues:
        lines.append("")
        lines.append("Issues:")

        for issue in report.issues:
            lines.append(f"- [{issue.code}] {issue.message}")

    if report.warnings:
        lines.append("")
        lines.append("Warnings:")

        for warning in report.warnings:
            lines.append(f"- [{warning.code}] {warning.message}")

    return "\n".join(lines)


def parse_args(
    argv: Sequence[str] | None = None,
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate the latest saved analysis for an application."
        )
    )

    parser.add_argument(
        "application_id",
        help="Application UUID to evaluate.",
    )

    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        application_id = uuid.UUID(args.application_id)
    except ValueError:
        print(
            "application_id must be a valid UUID.",
            file=sys.stderr,
        )
        return 2

    with SessionLocal() as db:
        try:
            report = evaluate_saved_analysis(
                db=db,
                application_id=application_id,
            )
        except EvaluationTargetNotFoundError as exc:
            print(str(exc), file=sys.stderr)
            return 2

    print(format_evaluation_report(report))

    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())