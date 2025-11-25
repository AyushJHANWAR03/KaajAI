"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI
    openai_api_key: str
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.3
    llm_max_tokens: int = 1000

    # Database
    database_url: str = "sqlite:///./kaaj_analyzer.db"  # Default to SQLite for MVP

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "*"  # Allow all origins for deployment

    # File Storage
    upload_dir: str = "/tmp/uploads"
    max_file_size: int = 10485760  # 10MB

    class Config:
        # Look for .env in parent directory (project root)
        env_file = str(Path(__file__).parent.parent.parent / ".env")
        case_sensitive = False
        extra = "ignore"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()
