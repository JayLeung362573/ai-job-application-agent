import json
from collections.abc import Sequence
from typing import Any

from openai import APIError, OpenAI

from app.schemas.analysis import AnalysisResult
from app.services.analysis.provider import ResumeProjectContext


class OpenAIAnalysisProviderError(RuntimeError):
    """Raised when the OpenAI provider cannot return a valid analysis."""


class OpenAIAnalysisProvider:
    """Generate structured job analyses with the OpenAI API."""

    SYSTEM_PROMPT = """
You are a resume match assistant for software engineering internships.

Analyze the job description against the provided resume projects.

Rules:
- Return only data that fits the provided structured schema.
- Do not invent projects that are not included in the resume project list.
- Use concise, interview-focused wording.
- Match skills only when they are clearly supported by the project context.
- Suggested bullets should be resume-ready and action-oriented.
- Interview questions should be specific to the matched projects.
- The match score must be an integer from 0 to 100.
""".strip()

    def __init__(
        self,
        *,
        client: Any | None = None,
        model: str = "gpt-5.5",
        api_key: str | None = None,
    ) -> None:
        client_kwargs: dict[str, str] = {}

        if api_key is not None:
            client_kwargs["api_key"] = api_key

        self.client = client or OpenAI(**client_kwargs)
        self.model = model

    def analyze(
        self,
        *,
        job_description: str,
        resume_projects: Sequence[ResumeProjectContext],
    ) -> AnalysisResult:
        normalized_description = job_description.strip()

        if not normalized_description:
            raise ValueError("Job description cannot be empty.")

        user_prompt = self._build_user_prompt(
            job_description=normalized_description,
            resume_projects=resume_projects,
        )

        try:
            response = self.client.responses.parse(
                model=self.model,
                input=[
                    {
                        "role": "system",
                        "content": self.SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                text_format=AnalysisResult,
            )
        except APIError as exc:
            raise OpenAIAnalysisProviderError(
                "OpenAI analysis request failed."
            ) from exc

        parsed_result = response.output_parsed

        if not isinstance(parsed_result, AnalysisResult):
            raise OpenAIAnalysisProviderError(
                "OpenAI response did not match the expected analysis schema."
            )

        return parsed_result

    @staticmethod
    def _build_user_prompt(
        *,
        job_description: str,
        resume_projects: Sequence[ResumeProjectContext],
    ) -> str:
        project_payload = [
            {
                "name": project.name,
                "tech_stack": list(project.tech_stack),
                "description": project.description,
                "resume_bullets": list(project.resume_bullets),
            }
            for project in resume_projects
        ]

        return (
            "Job description:\n"
            f"{job_description}\n\n"
            "Resume projects:\n"
            f"{json.dumps(project_payload, indent=2, ensure_ascii=False)}"
        )