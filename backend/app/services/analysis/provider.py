from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from app.schemas.analysis import AnalysisResult

class AnalysisProviderError(RuntimeError):
    """Raised when an analysis provider cannot complete a request."""


@dataclass(frozen=True, slots=True)
class ResumeProjectContext:
    name: str
    tech_stack: tuple[str, ...]
    description: str
    resume_bullets: tuple[str, ...]


class AnalysisProvider(Protocol):
    def analyze(
        self,
        *,
        job_description: str,
        resume_projects: Sequence[ResumeProjectContext],
    ) -> AnalysisResult:
        """Analyze a job description against the supplied resume projects."""
        ...