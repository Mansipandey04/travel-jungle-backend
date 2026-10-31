"""Application settings — placeholders only; never commit real secrets."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Travel Jungle API"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://travel:travel@db:5432/travel_jungle"
    admin_api_token: str = "change-me-admin-token"
    cors_origins: str = "http://localhost:3000"
    rate_limit_submissions_per_min: int = 5
    upload_root: str = "/data/uploads"
    upload_max_bytes: int = 5 * 1024 * 1024
    seed_demo: bool = False
    public_base_url: str = "http://localhost:8000"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
