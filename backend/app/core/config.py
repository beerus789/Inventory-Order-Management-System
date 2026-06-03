"""Application configuration management."""

import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = os.getenv("APP_NAME", "Inventory Order Management API")
    app_env: str = os.getenv("APP_ENV", "development")
    app_debug: bool = os.getenv("APP_DEBUG", "true").lower() == "true"

    # Database
    database_host: str = os.getenv("DATABASE_HOST", "db")
    database_port: int = int(os.getenv("DATABASE_PORT", "5432"))
    database_name: str = os.getenv("DATABASE_NAME", "inventory_db")
    database_user: str = os.getenv("DATABASE_USER", "postgres")
    database_password: str = os.getenv("DATABASE_PASSWORD", "postgres")
    database_sslmode: str = os.getenv("DATABASE_SSLMODE", "require")
    database_url: Optional[str] = os.getenv("DATABASE_URL")

    # Derived database URL if not provided
    @property
    def sqlalchemy_database_url(self) -> str:
        """Get SQLAlchemy database URL."""
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+psycopg://{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
            f"?sslmode={self.database_sslmode}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
