import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MatchedProject(BaseModel):
    project_name: str = Field(min_length=1, max_length=255)
    matched_skills: list[str]
    reason: str = Field(min_length=1)


class SuggestedBullet(BaseModel):
    project_name: str = Field(min_length=1, max_length=255)
    bullet: str = Field(min_length=1)
    target_skill: str = Field(min_length=1, max_length=255)


class AnalysisResult(BaseModel):
    required_skills: list[str]
    preferred_skills: list[str]
    responsibilities: list[str]
    matched_projects: list[MatchedProject]
    missing_skills: list[str]
    suggested_bullets: list[SuggestedBullet]
    interview_questions: list[str]
    match_score: int = Field(ge=0, le=100)


class AnalysisRead(AnalysisResult):
    id: uuid.UUID
    application_id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)