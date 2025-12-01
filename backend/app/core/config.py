"""Application configuration settings."""
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database
    DATABASE_URL: str = "sqlite:///./aeropdf.db"

    # Storage directories
    STORAGE_DIR: str = "storage"
    PDF_DIR: str = "storage/pdfs"
    RENDER_DIR: str = "storage/renders"

    # Application
    DEBUG: bool = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Create storage directories if they don't exist."""
        Path(self.STORAGE_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.PDF_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.RENDER_DIR).mkdir(parents=True, exist_ok=True)


settings = Settings()

