from fastapi import Header, HTTPException, status
from secrets import compare_digest
from typing import Annotated

from app.core.config import get_settings
from app.services.analysis import (
    AnalysisService,
    MockAnalysisProvider,
    OpenAIAnalysisProvider,
)

def require_analysis_access_token(
    x_analysis_access_token: Annotated[
        str | None,
        Header(),
    ] = None,
) -> None:
    settings = get_settings()

    if settings.analysis_provider != "openai":
        return

    expected_token = settings.analysis_access_token

    if expected_token is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Analysis access control unavailable",
        )

    if (
        x_analysis_access_token is None
        or not compare_digest(
            x_analysis_access_token.encode("utf-8"),
            expected_token.encode("utf-8"),
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid analysis access token",
        )

def get_analysis_service() -> AnalysisService:
    settings = get_settings()

    if settings.analysis_provider == "openai":
        if settings.openai_api_key is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Analysis provider unavailable",
            )

        provider = OpenAIAnalysisProvider(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
        )
    else:
        provider = MockAnalysisProvider()

    return AnalysisService(provider=provider)