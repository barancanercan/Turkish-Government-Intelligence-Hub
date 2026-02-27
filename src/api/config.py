"""
API Configuration
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings."""
    
    APP_NAME: str = "MIZAN-AI API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8501"]
    
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    API_KEY_HEADER: str = "X-API-Key"
    
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_DAY: int = 1000
    
    FREE_TIER_DAILY: int = 10
    PRO_TIER_DAILY: int = 500
    ENTERPRISE_TIER_DAILY: int = -1
    
    REDIS_URL: str = "redis://localhost:6379"
    
    GEMINI_API_KEY: str = ""
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
