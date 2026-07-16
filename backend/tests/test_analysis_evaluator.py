from app.schemas.analysis import AnalysisResult
from app.services.analysis import (
    ResumeProjectContext,
    evaluate_analysis_result,
)


PROJECTS = [
    ResumeProjectContext(
        name="Smart Farm IoT Data Pipeline",
        tech_stack=(
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Docker",
        ),
        description=(
            "A backend telemetry pipeline using FastAPI and PostgreSQL."
        ),
        resume_bullets=(
            "Built a containerized FastAPI telemetry service.",
            "Stored sensor readings in PostgreSQL.",
        ),
    ),
    ResumeProjectContext(
        name="C++ WebSocket Multiplayer Game Server",
        tech_stack=(
            "C++23",
            "WebSockets",
            "GoogleTest",
        ),
        description="A multiplayer game server using WebSockets.",
        resume_bullets=(
            "Implemented server-authoritative lobby flows.",
        ),
    ),
]


def create_valid_analysis_result() -> AnalysisResult:
    return AnalysisResult(
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
                    "The project demonstrates backend API development "
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


def issue_codes(result: AnalysisResult) -> set[str]:
    report = evaluate_analysis_result(
        result=result,
        resume_projects=PROJECTS,
    )

    return {
        issue.code
        for issue in report.issues
    }


def warning_codes(result: AnalysisResult) -> set[str]:
    report = evaluate_analysis_result(
        result=result,
        resume_projects=PROJECTS,
    )

    return {
        warning.code
        for warning in report.warnings
    }


def test_evaluator_accepts_grounded_analysis_result() -> None:
    result = create_valid_analysis_result()

    report = evaluate_analysis_result(
        result=result,
        resume_projects=PROJECTS,
    )

    assert report.passed is True
    assert report.issues == ()


def test_evaluator_rejects_unknown_matched_project() -> None:
    result = create_valid_analysis_result()
    result.matched_projects[0].project_name = "Invented Project"

    assert "unknown_matched_project" in issue_codes(result)


def test_evaluator_rejects_unsupported_matched_skill() -> None:
    result = create_valid_analysis_result()
    result.matched_projects[0].matched_skills.append("Kubernetes")

    assert "unsupported_matched_skill" in issue_codes(result)


def test_evaluator_rejects_missing_skill_that_is_covered() -> None:
    result = create_valid_analysis_result()
    result.missing_skills.append("PostgreSQL")

    assert "covered_skill_marked_missing" in issue_codes(result)


def test_evaluator_rejects_unknown_suggestion_project() -> None:
    result = create_valid_analysis_result()
    result.suggested_bullets[0].project_name = "Fake Project"

    assert "unknown_suggestion_project" in issue_codes(result)


def test_evaluator_warns_for_short_suggested_bullet() -> None:
    result = create_valid_analysis_result()
    result.suggested_bullets[0].bullet = "Used FastAPI."

    assert "short_suggested_bullet" in warning_codes(result)


def test_evaluator_rejects_missing_interview_questions() -> None:
    result = create_valid_analysis_result()
    result.interview_questions = []

    assert "missing_interview_questions" in issue_codes(result)


def test_evaluator_supports_partial_skill_matches() -> None:
    result = AnalysisResult(
        required_skills=[
            "C++",
            "WebSockets",
        ],
        preferred_skills=[],
        responsibilities=[
            "Build networking systems.",
        ],
        matched_projects=[
            {
                "project_name": (
                    "C++ WebSocket Multiplayer Game Server"
                ),
                "matched_skills": [
                    "C++",
                    "WebSockets",
                ],
                "reason": (
                    "The project demonstrates C++ networking work."
                ),
            }
        ],
        missing_skills=[],
        suggested_bullets=[
            {
                "project_name": (
                    "C++ WebSocket Multiplayer Game Server"
                ),
                "bullet": (
                    "Implemented a C++ WebSocket game server with "
                    "server-authoritative session flows."
                ),
                "target_skill": "C++",
            }
        ],
        interview_questions=[
            (
                "How did you design the C++ WebSocket server?"
            ),
        ],
        match_score=90,
    )

    report = evaluate_analysis_result(
        result=result,
        resume_projects=PROJECTS,
    )

    assert report.passed is True