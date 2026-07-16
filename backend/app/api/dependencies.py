from fastapi import HTTPException, status

from app.core.config import get_settings
from app.services.analysis import (
    AnalysisService,
    MockAnalysisProvider,
    OpenAIAnalysisProvider,
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