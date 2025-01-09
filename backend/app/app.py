# backend/app/app.py
from fastapi import FastAPI
from .core.logger import setup_logger
from .core.config import get_settings
from .core.db import get_db
from . import __version__

# Setup logging first
logger = setup_logger(__name__)
logger.debug("----------------------------------- RESTART----------------------------------------")
# Load settings
settings = get_settings()
logger.debug("Settings:")
for key, value in settings.model_dump().items():
    logger.debug(f"  - {key}: {value}")

with get_db() as db:
    logger.debug("Database connection established")
    #get_db_info()

app = FastAPI(
    title=settings.APP_NAME,
    version=__version__,
    debug=settings.DEBUG,
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.debug("Health check endpoint called")
    return {
        "status": "healthy",
        "version": __version__
    }

# Include routers
# app.include_router(
#     some_router,
#     prefix=settings.API_V1_PREFIX
# )
