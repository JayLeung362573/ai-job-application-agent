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

def test_database_urls_use_psycopg_driver() -> None:
    settings = Settings(
        database_url=(
            "postgresql://user:password@pooled.example.com/database"
        ),
        database_url_unpooled=(
            "postgres://user:password@direct.example.com/database"
        ),
        _env_file=None,
    )

    assert settings.database_url == (
        "postgresql+psycopg://"
        "user:password@pooled.example.com/database"
    )
    assert settings.database_url_unpooled == (
        "postgresql+psycopg://"
        "user:password@direct.example.com/database"
    )


def test_migration_url_prefers_unpooled_database_url() -> None:
    settings = Settings(
        database_url="postgresql://user:password@pooled/database",
        database_url_unpooled=(
            "postgresql://user:password@direct/database"
        ),
        _env_file=None,
    )

    assert settings.migration_database_url == (
        "postgresql+psycopg://user:password@direct/database"
    )


def test_migration_url_falls_back_to_database_url() -> None:
    settings = Settings(
        database_url="postgresql://user:password@database/db",
        database_url_unpooled=None,
        _env_file=None,
    )

    assert settings.migration_database_url == (
        "postgresql+psycopg://user:password@database/db"
    )