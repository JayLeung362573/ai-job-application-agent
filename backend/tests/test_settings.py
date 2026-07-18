from app.core.config import Settings


def test_cors_origins_default_to_local_frontend() -> None:
    settings = Settings(_env_file=None)

    assert settings.cors_origin_list == ["http://localhost:3000"]


def test_cors_origins_support_multiple_urls(
    monkeypatch,
) -> None:
    monkeypatch.setenv(
        "CORS_ORIGINS",
        "https://frontend.vercel.app, https://preview.vercel.app",
    )

    settings = Settings(_env_file=None)

    assert settings.cors_origin_list == [
        "https://frontend.vercel.app",
        "https://preview.vercel.app",
    ]