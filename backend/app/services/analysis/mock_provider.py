from collections.abc import Sequence

from app.schemas.analysis import (
    AnalysisResult,
    MatchedProject,
    SuggestedBullet,
)
from app.services.analysis.provider import ResumeProjectContext


class MockAnalysisProvider:
    """Generate deterministic analysis results without calling an AI API."""

    KNOWN_SKILLS: tuple[str, ...] = (
        "Python",
        "FastAPI",
        "PostgreSQL",
        "Docker",
        "GitHub Actions",
        "TypeScript",
        "React",
        "Next.js",
        "C++",
        "MPI",
        "WebSockets",
        "GoogleTest",
    )

    def analyze(
        self,
        *,
        job_description: str,
        resume_projects: Sequence[ResumeProjectContext],
    ) -> AnalysisResult:
        normalized_description = job_description.strip()

        if not normalized_description:
            raise ValueError("Job description cannot be empty.")

        required_skills = self._extract_required_skills(
            normalized_description
        )

        matched_projects: list[MatchedProject] = []
        suggested_bullets: list[SuggestedBullet] = []
        matched_required_skills: set[str] = set()
        interview_questions: list[str] = []

        for project in resume_projects:
            project_matches = self._get_project_matches(
                required_skills=required_skills,
                project=project,
            )

            if not project_matches:
                continue

            matched_required_skills.update(project_matches)

            matched_projects.append(
                MatchedProject(
                    project_name=project.name,
                    matched_skills=project_matches,
                    reason=(
                        f"{project.name} demonstrates experience with "
                        f"{', '.join(project_matches)}."
                    ),
                )
            )

            if project.resume_bullets:
                suggested_bullets.append(
                    SuggestedBullet(
                        project_name=project.name,
                        bullet=project.resume_bullets[0],
                        target_skill=project_matches[0],
                    )
                )

            interview_questions.append(
                (
                    f"How did you use {project_matches[0]} "
                    f"in {project.name}?"
                )
            )

        missing_skills = [
            skill
            for skill in required_skills
            if skill not in matched_required_skills
        ]

        match_score = self._calculate_match_score(
            required_skills=required_skills,
            matched_skills=matched_required_skills,
        )

        return AnalysisResult(
            required_skills=required_skills,
            preferred_skills=[],
            responsibilities=[
                (
                    "Build and maintain software aligned with the "
                    "job requirements."
                ),
                (
                    "Collaborate with engineers and communicate "
                    "technical decisions."
                ),
            ],
            matched_projects=matched_projects,
            missing_skills=missing_skills,
            suggested_bullets=suggested_bullets,
            interview_questions=interview_questions,
            match_score=match_score,
        )

    def _extract_required_skills(
        self,
        job_description: str,
    ) -> list[str]:
        normalized_description = job_description.casefold()

        return [
            skill
            for skill in self.KNOWN_SKILLS
            if skill.casefold() in normalized_description
        ]

    def _get_project_matches(
        self,
        *,
        required_skills: Sequence[str],
        project: ResumeProjectContext,
    ) -> list[str]:
        return [
            required_skill
            for required_skill in required_skills
            if any(
                self._skills_match(
                    required_skill,
                    project_skill,
                )
                for project_skill in project.tech_stack
            )
        ]

    @staticmethod
    def _skills_match(
        required_skill: str,
        project_skill: str,
    ) -> bool:
        normalized_required = required_skill.casefold()
        normalized_project = project_skill.casefold()

        return (
            normalized_required == normalized_project
            or normalized_required in normalized_project
            or normalized_project in normalized_required
        )

    @staticmethod
    def _calculate_match_score(
        *,
        required_skills: Sequence[str],
        matched_skills: set[str],
    ) -> int:
        if not required_skills:
            return 0

        return round(
            len(matched_skills)
            / len(required_skills)
            * 100
        )