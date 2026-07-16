import pytest
from pydantic import ValidationError

from app.api.dependencies import get_analysis_service
from app.core.config import get_settings
from app.services.analysis import (
    MockAnalysisProvider,
    OpenAIAnalysisProvider,
)


@pytest.fixture(autouse=True)
def clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_settings_default_to_mock_provider(monkeypatch) -> None:
    monkeypatch.delenv("ANALYSIS_PROVIDER", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    settings = get_settings()

    assert settings.analysis_provider == "mock"
    assert settings.openai_model == "gpt-5.5"
    assert settings.openai_api_key is None


def test_settings_accept_openai_provider(monkeypatch) -> None:
    monkeypatch.setenv("ANALYSIS_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    settings = get_settings()

    assert settings.analysis_provider == "openai"
    assert settings.openai_model == "test-model"
    assert settings.openai_api_key == "test-key"


def test_settings_reject_invalid_provider(monkeypatch) -> None:
    monkeypatch.setenv("ANALYSIS_PROVIDER", "invalid-provider")

    with pytest.raises(ValidationError):
        get_settings()


def test_empty_openai_api_key_is_treated_as_none(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "   ")

    settings = get_settings()

    assert settings.openai_api_key is None


def test_dependency_uses_mock_provider_by_default(monkeypatch) -> None:
    monkeypatch.delenv("ANALYSIS_PROVIDER", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    service = get_analysis_service()

    assert isinstance(service.provider, MockAnalysisProvider)


def test_dependency_can_select_openai_provider(monkeypatch) -> None:
    monkeypatch.setenv("ANALYSIS_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    service = get_analysis_service()

    assert isinstance(service.provider, OpenAIAnalysisProvider)
    assert service.provider.model == "test-model"