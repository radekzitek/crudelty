# backend/app/core/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Determine environment
ENV = os.getenv("ENV", "development")

# Load appropriate .env file
env_file = f".env.{ENV}" if os.path.exists(f".env.{ENV}") else ".env"

load_dotenv(env_file)

class Settings(BaseSettings):
    """Application settings"""
    # App settings
    APP_NAME: str 
    DEBUG: bool 
    API_V1_PREFIX: str 
    
    # Database settings
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # Logging
    LOG_CONSOLE: bool
    LOG_LEVEL: str 
    LOG_FORMAT: str 
    LOG_FILE: Optional[str] 
    LOG_ROTATE_SIZE: int 
    LOG_ROTATE_BACKUPS: int 
    LOG_ROTATE_DAYS: int 
    LOG_ROTATE_WHEN: str 
    LOG_ROTATE_INTERVAL: int 
    
    class Config:
        env_file = env_file
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()