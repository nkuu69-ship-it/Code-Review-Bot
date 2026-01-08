from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "AI Code Review Bot API"
    API_V1_STR: str = "/api"
    DEBUG: bool = False
    
    # LLM Config
    HUGGINGFACE_API_TOKEN: str
    MODEL_NAME: str = "meta-llama/Meta-Llama-3-8B-Instruct"
    
    # Safety Limits
    MAX_CODE_LENGTH: int = 10000  # Max characters per file
    REQUEST_TIMEOUT: int = 30     # Seconds

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8", 
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
