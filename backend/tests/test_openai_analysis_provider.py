from types import SimpleNamespace
from typing import Any

import pytest

from app.schemas.analysis import AnalysisResult
from app.services.analysis import ResumeProjectContext
from app.services.analysis.openai_provider import (
    OpenAIAnalysisProvider,
    OpenAIAnalysisProviderError,
)


def create_analysis_result() -> AnalysisResult:
    return AnalysisResult(
        required_skills=[
            "Python",
            "FastAPI",
            "React",
        ],
        preferred_skills=[],
        responsibilities=[
            "Build and maintain backend APIs.",
        ],
        matched_projects=[
            {
                "project_name": "Smart Farm IoT Data Pipeline",
                "matched_skills": [
                    "Python",
                    "FastAPI",
                ],
                "reason": (
                    "The project demonstrates backend API design "
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
                    "Built a FastAPI telemetry service backed by "
                    "PostgreSQL."
                ),
                "target_skill": "FastAPI",
            }
        ],
        interview_questions=[
            "How did you design the FastAPI service?",
        ],
        match_score=67,
    )


class FakeResponses:
    def __init__(self, parsed_result: Any) -> None:
        self.parsed_result = parsed_result
        self.calls: list[dict[str, Any]] = []

    def parse(self, **kwargs: Any) -> SimpleNamespace:
        self.calls.append(kwargs)

        return SimpleNamespace(
            output_parsed=self.parsed_result,
        )


class FakeOpenAIClient:
    def __init__(self, parsed_result: Any) -> None:
        self.responses = FakeResponses(parsed_result)


PROJECTS = [
    ResumeProjectContext(
        name="Smart Farm IoT Data Pipeline",
        tech_stack=(
            "Python",
            "FastAPI",
            "PostgreSQL",
        ),
        description="A backend telemetry pipeline.",
        resume_bullets=(
            "Built a FastAPI telemetry pipeline.",
        ),
    )
]


def test_openai_provider_returns_parsed_analysis_result() -> None:
    parsed_result = create_analysis_result()
    fake_client = FakeOpenAIClient(parsed_result)

    provider = OpenAIAnalysisProvider(
        client=fake_client,
        model="test-model",
    )

    result = provider.analyze(
        job_description=(
            "Python backend role requiring FastAPI and React."
        ),
        resume_projects=PROJECTS,
    )

    assert result == parsed_result

    assert len(fake_client.responses.calls) == 1

    call = fake_client.responses.calls[0]

    assert call["model"] == "test-model"
    assert call["text_format"] is AnalysisResult

    assert call["input"][0]["role"] == "system"
    assert "resume match assistant" in call["input"][0]["content"]

    assert call["input"][1]["role"] == "user"
    assert "Python backend role" in call["input"][1]["content"]
    assert "Smart Farm IoT Data Pipeline" in call["input"][1]["content"]


def test_openai_provider_rejects_empty_job_description() -> None:
    fake_client = FakeOpenAIClient(create_analysis_result())

    provider = OpenAIAnalysisProvider(
        client=fake_client,
        model="test-model",
    )

    with pytest.raises(
        ValueError,
        match="Job description cannot be empty",
    ):
        provider.analyze(
            job_description="   ",
            resume_projects=PROJECTS,
        )

    assert fake_client.responses.calls == []


def test_openai_provider_rejects_unparsed_response() -> None:
    fake_client = FakeOpenAIClient(parsed_result=None)

    provider = OpenAIAnalysisProvider(
        client=fake_client,
        model="test-model",
    )

    with pytest.raises(
        OpenAIAnalysisProviderError,
        match="expected analysis schema",
    ):
        provider.analyze(
            job_description="Python backend role.",
            resume_projects=PROJECTS,
        )