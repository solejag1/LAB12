"""Application settings loaded from environment variables."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Main application configuration."""

    DATABASE_URL: str = "sqlite+aiosqlite:///./bank.db"
    SECRET_KEY: str = "change-me-to-a-random-32-char-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    APP_NAME: str = "Banking Application"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "bank_db"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()  # type: ignore[call-arg]
