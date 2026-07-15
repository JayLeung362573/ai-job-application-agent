import pytest
from pydantic import ValidationError

from app.schemas.analysis import AnalysisResult


VALID_ANALYSIS_DATA = {
    "required_skills": [
        "Python",
        "FastAPI",
        "PostgreSQL",
        "Docker",
    ],
    "preferred_skills": [
        "React",
        "TypeScript",
    ],
    "responsibilities": [
        "Build backend APIs.",
        "Collaborate with frontend engineers.",
    ],
    "matched_projects": [
        {
            "project_name": "Smart Farm IoT Data Pipeline",
            "matched_skills": [
                "Python",
                "FastAPI",
                "PostgreSQL",
                "Docker",
            ],
            "reason": (
                "The project demonstrates backend API development, "
                "database design, and containerized deployment."
            ),
        }
    ],
    "missing_skills": [
        "React",
        "TypeScript",
    ],
    "suggested_bullets": [
        {
            "project_name": "Smart Farm IoT Data Pipeline",
            "bullet": (
                "Built a containerized FastAPI telemetry service backed "
                "by partitioned PostgreSQL storage."
            ),
            "target_skill": "Backend API development",
        }
    ],
    "interview_questions": [
        "How did you design the telemetry ingestion pipeline?",
        "Why did you choose BRIN indexes?",
    ],
    "match_score": 78,
}


def test_analysis_result_accepts_valid_structured_data() -> None:
    result = AnalysisResult.model_validate(VALID_ANALYSIS_DATA)

    assert result.match_score == 78
    assert result.required_skills == [
        "Python",
        "FastAPI",
        "PostgreSQL",
        "Docker",
    ]

    assert len(result.matched_projects) == 1

    matched_project = result.matched_projects[0]

    assert matched_project.project_name == (
        "Smart Farm IoT Data Pipeline"
    )
    assert "FastAPI" in matched_project.matched_skills

    assert len(result.suggested_bullets) == 1
    assert (
        result.suggested_bullets[0].target_skill
        == "Backend API development"
    )


def test_analysis_result_rejects_score_above_100() -> None:
    invalid_data = {
        **VALID_ANALYSIS_DATA,
        "match_score": 101,
    }

    with pytest.raises(ValidationError):
        AnalysisResult.model_validate(invalid_data)


def test_analysis_result_rejects_invalid_matched_project() -> None:
    invalid_data = {
        **VALID_ANALYSIS_DATA,
        "matched_projects": [
            {
                "project_name": "Smart Farm IoT Data Pipeline",
                "matched_skills": ["Python"],
                # reason is intentionally missing
            }
        ],
    }

    with pytest.raises(ValidationError):
        AnalysisResult.model_validate(invalid_data)