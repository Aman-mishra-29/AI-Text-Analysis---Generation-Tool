from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from pydantic import Field
from typing import List

print("👍 Working")


# ---------------------------------------------------
# Base Settings Class
# ---------------------------------------------------
class Settings(BaseSettings):

    # App Info
    APP_NAME: str = Field(default="Text AI Tool API")
    APP_VERSION: str = Field(default="1.0.0")
    DEBUG: bool = Field(default=True)

    # API Config
    API_V1_PREFIX: str = Field(default="/api/v1")
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)

    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Model
    SUMMARIZATION_MODEL: str = Field(default="facebook/bart-large-cnn")
    MAX_SUMMARY_LENGTH: int = Field(default=130)
    MIN_SUMMARY_LENGTH: int = Field(default=30)

    # Plagiarism
    USE_SEMANTIC_SIMILARITY: bool = Field(default=True)

    # Autocorrect
    LANGUAGE_TOOL_LANG: str = Field(default="en-US")

    # MongoDB
    MONGO_URI: str = Field(default="mongodb://localhost:27017")
    DATABASE_NAME: str = Field(default="text_ai_db")

    # Logging
    LOG_LEVEL: str = Field(default="INFO")

    # Security
    SECRET_KEY: str = Field(default="super-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)

    # Limits
    MAX_TEXT_LENGTH: int = Field(default=5000)
    REQUEST_TIMEOUT: int = Field(default=30)

    # .env support
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"   # ✅ THIS FIXES YOUR ERROR
    )


# ---------------------------------------------------
# Cached Settings
# ---------------------------------------------------
@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()