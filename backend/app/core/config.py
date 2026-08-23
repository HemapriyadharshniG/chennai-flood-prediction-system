"""Application configuration settings using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings and environment variable configuration."""

    database_url: str = "postgresql://floodadmin:floodpass@localhost:5432/chennai_flood"
    cors_allowed_origins: str = "http://localhost:3000,http://localhost:5173"
    openweathermap_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
