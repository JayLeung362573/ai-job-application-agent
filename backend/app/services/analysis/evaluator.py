from collections.abc import Sequence
from dataclasses import dataclass

from app.schemas.analysis import AnalysisResult
from app.services.analysis.provider import ResumeProjectContext


@dataclass(frozen=True, slots=True)
class AnalysisEvaluationIssue:
    code: str
    message: str


@dataclass(frozen=True, slots=True)
class AnalysisEvaluationReport:
    issues: tuple[AnalysisEvaluationIssue, ...]
    warnings: tuple[AnalysisEvaluationIssue, ...]

    @property
    def passed(self) -> bool:
        return len(self.issues) == 0


def evaluate_analysis_result(
    *,
    result: AnalysisResult,
    resume_projects: Sequence[ResumeProjectContext],
) -> AnalysisEvaluationReport:
    issues: list[AnalysisEvaluationIssue] = []
    warnings: list[AnalysisEvaluationIssue] = []

    project_contexts = {
        project.name: project
        for project in resume_projects
    }

    all_supported_skills = {
        normalized_skill
        for project in resume_projects
        for normalized_skill in _normalized_project_skills(project)
    }

    if not result.required_skills:
        warnings.append(
            AnalysisEvaluationIssue(
                code="no_required_skills",
                message="The analysis did not identify any required skills.",
            )
        )

    if not result.responsibilities:
        warnings.append(
            AnalysisEvaluationIssue(
                code="no_responsibilities",
                message="The analysis did not identify any responsibilities.",
            )
        )

    for matched_project in result.matched_projects:
        project = project_contexts.get(matched_project.project_name)

        if project is None:
            issues.append(
                AnalysisEvaluationIssue(
                    code="unknown_matched_project",
                    message=(
                        "Matched project is not present in the supplied "
                        f"resume projects: {matched_project.project_name}"
                    ),
                )
            )
            continue

        if not matched_project.matched_skills:
            warnings.append(
                AnalysisEvaluationIssue(
                    code="matched_project_without_skills",
                    message=(
                        "Matched project has no matched skills: "
                        f"{matched_project.project_name}"
                    ),
                )
            )

        supported_skills = _normalized_project_skills(project)

        for skill in matched_project.matched_skills:
            if not _skill_is_supported(
                skill=skill,
                supported_skills=supported_skills,
                project=project,
            ):
                issues.append(
                    AnalysisEvaluationIssue(
                        code="unsupported_matched_skill",
                        message=(
                            f"Skill '{skill}' is not supported by project "
                            f"'{matched_project.project_name}'."
                        ),
                    )
                )

    for missing_skill in result.missing_skills:
        if _normalize(missing_skill) in all_supported_skills:
            issues.append(
                AnalysisEvaluationIssue(
                    code="covered_skill_marked_missing",
                    message=(
                        f"Skill '{missing_skill}' is marked missing but is "
                        "covered by at least one resume project."
                    ),
                )
            )

    required_or_preferred_skills = {
        _normalize(skill)
        for skill in [
            *result.required_skills,
            *result.preferred_skills,
        ]
    }

    for suggestion in result.suggested_bullets:
        if suggestion.project_name not in project_contexts:
            issues.append(
                AnalysisEvaluationIssue(
                    code="unknown_suggestion_project",
                    message=(
                        "Suggested bullet references an unknown project: "
                        f"{suggestion.project_name}"
                    ),
                )
            )

        if (
            required_or_preferred_skills
            and _normalize(suggestion.target_skill)
            not in required_or_preferred_skills
        ):
            warnings.append(
                AnalysisEvaluationIssue(
                    code="suggestion_targets_non_required_skill",
                    message=(
                        f"Suggested bullet targets '{suggestion.target_skill}', "
                        "which was not listed as a required or preferred skill."
                    ),
                )
            )

        if len(suggestion.bullet.strip()) < 30:
            warnings.append(
                AnalysisEvaluationIssue(
                    code="short_suggested_bullet",
                    message=(
                        "Suggested bullet may be too short to be useful: "
                        f"{suggestion.bullet}"
                    ),
                )
            )

    if result.matched_projects and not result.interview_questions:
        issues.append(
            AnalysisEvaluationIssue(
                code="missing_interview_questions",
                message=(
                    "The analysis matched projects but did not generate "
                    "interview questions."
                ),
            )
        )

    if not result.matched_projects and result.match_score > 50:
        warnings.append(
            AnalysisEvaluationIssue(
                code="high_score_without_project_matches",
                message=(
                    "The analysis has a high score but no matched projects."
                ),
            )
        )

    return AnalysisEvaluationReport(
        issues=tuple(issues),
        warnings=tuple(warnings),
    )


def _normalize(value: str) -> str:
    return value.casefold().strip()


def _normalized_project_skills(
    project: ResumeProjectContext,
) -> set[str]:
    return {
        _normalize(skill)
        for skill in project.tech_stack
    }


def _skill_is_supported(
    *,
    skill: str,
    supported_skills: set[str],
    project: ResumeProjectContext,
) -> bool:
    normalized_skill = _normalize(skill)

    if normalized_skill in supported_skills:
        return True

    if any(
        normalized_skill in supported_skill
        or supported_skill in normalized_skill
        for supported_skill in supported_skills
    ):
        return True

    searchable_project_text = _normalize(
        " ".join(
            [
                project.description,
                *project.resume_bullets,
            ]
        )
    )

    return normalized_skill in searchable_project_text