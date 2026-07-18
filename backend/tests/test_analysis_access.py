from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.api import dependencies


def set_analysis_settings(
    monkeypatch: pytest.MonkeyPatch,
    *,
    provider: str,
    token: str | None,
) -> None:
    monkeypatch.setattr(
        dependencies,
        "get_settings",
        lambda: SimpleNamespace(
            analysis_provider=provider,
            analysis_access_token=token,
        ),
    )


def test_mock_provider_does_not_require_access_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    set_analysis_settings(
        monkeypatch,
        provider="mock",
        token=None,
    )

    dependencies.require_analysis_access_token(None)


def test_openai_provider_requires_configured_access_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    set_analysis_settings(
        monkeypatch,
        provider="openai",
        token=None,
    )

    with pytest.raises(HTTPException) as exc_info:
        dependencies.require_analysis_access_token(None)

    assert exc_info.value.status_code == 503


def test_openai_provider_rejects_invalid_access_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    set_analysis_settings(
        monkeypatch,
        provider="openai",
        token="expected-token",
    )

    with pytest.raises(HTTPException) as exc_info:
        dependencies.require_analysis_access_token(
            "incorrect-token"
        )

    assert exc_info.value.status_code == 401


def test_openai_provider_accepts_valid_access_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    set_analysis_settings(
        monkeypatch,
        provider="openai",
        token="expected-token",
    )

    dependencies.require_analysis_access_token(
        "expected-token"
    )