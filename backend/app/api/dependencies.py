from app.services.analysis import (
    AnalysisService,
    MockAnalysisProvider,
)


def get_analysis_service() -> AnalysisService:
    return AnalysisService(
        provider=MockAnalysisProvider(),
    )