# backend/app/core/config.py
from logging import getLogger
from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

logger = getLogger(__name__)
logger.debug("About to load settings")

# Determine environment
ENV = os.getenv("ENV", "development")
logger.debug(f"Environment: {ENV}")
# Load appropriate .env file
env_file = f".env.{ENV}" if os.path.exists(f".env.{ENV}") else ".env"
logger.debug(f"Loading environment file: {env_file}")

load_dotenv(env_file)
logger.debug("Environment file loaded")
class Settings(BaseSettings):
    """Application settings"""
    # App settings
    APP_NAME: str 
    DEBUG: bool 
    API_V1_PREFIX: str 
    
    # Database settings
    DATABASE_URL: str
    DB_POOL_SIZE: int
    DB_MAX_OVERFLOW: int
    DB_POOL_TIMEOUT: int
    DB_POOL_RECYCLE: int
    DB_ECHO: bool
    DB_ECHO_POOL: bool
    DB_RETRY_LIMIT: int
    DB_RETRY_DELAY: int
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # Logging
    LOG_CONSOLE: bool
    LOG_LEVEL: str 
    LOG_FORMAT: str 
    LOG_FILE: Optional[str] 
    #LOG_ROTATE_SIZE: int 
    LOG_ROTATE_BACKUPS: int 
    #LOG_ROTATE_DAYS: int 
    LOG_ROTATE_WHEN: str 
    LOG_ROTATE_INTERVAL: int 
    
    class Config:
        env_file = env_file
        case_sensitive = True

def get_settings() -> Settings:
    """Get cached settings instance"""
    logger.debug("About to return settings")
    return Settings()