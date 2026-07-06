import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResumeProjectRead(BaseModel):
    id: uuid.UUID
    name: str
    tech_stack: list[str]
    description: str
    resume_bullets: list[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)