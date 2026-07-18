from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


AnalysisProviderName = Literal["mock", "openai"]


class Settings(BaseSettings):
    database_url: str = (
        "postgresql+psycopg://jobagent:jobagent@localhost:5432/jobagent"
    )
    analysis_provider: AnalysisProviderName = "mock"
    openai_model: str = "gpt-5.5"
    openai_api_key: str | None = None
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("openai_api_key", mode="before")
    @classmethod
    def empty_api_key_to_none(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            return None

        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()