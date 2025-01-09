# backend/app/app.py
from fastapi import FastAPI, Query
from .core.logger import setup_logger
from .core.config import get_settings
from .api.v1 import api_router
from .core.middleware import LoggingMiddleware
from .core.metrics import get_metrics
from .core.redis_logger import redis_logger
from .core.db import get_db_session, check_db_health
from datetime import datetime
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

logger = setup_logger(__name__)
settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="Organization Management API",
    # OpenAPI configuration
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  # Hide schemas section by default
        "operationsSorter": "method",    # Sort operations by HTTP method
        "tagsSorter": "alpha",           # Sort tags alphabetically
        "docExpansion": "list",          # Show operations expanded
        "filter": True                    # Enable filtering operations
    },
    # Additional metadata
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "Private License",
    }
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Include API router with version prefix
app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX
)

@app.get("/health", tags=["System"])
async def health_check(db: AsyncSession = Depends(get_db_session)):
    """Health check endpoint"""
    # Check Redis
    redis_status = "healthy"
    try:
        await redis_logger.connect()
        await redis_logger.redis.ping()
    except Exception as e:
        redis_status = f"unhealthy: {str(e)}"

    # Check Database
    db_healthy, db_message = await check_db_health(db)
    db_status = "healthy" if db_healthy else f"unhealthy: {db_message}"

    # Overall status is healthy only if all components are healthy
    overall_status = "healthy" if (redis_status == "healthy" and db_healthy) else "unhealthy"

    return {
        "status": overall_status,
        "redis": redis_status,
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.1.0"
    }

@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API information and links"""
    return {
        "message": "Organization Management API",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi_json": "/openapi.json"
        },
        "version": "0.1.0",
        "status": "active"
    }

@app.get("/metrics", tags=["System"])
async def metrics():
    """Get API metrics"""
    return get_metrics()

@app.get("/logs", tags=["System"])
async def get_logs(
    level: str = None,
    request_id: str = None,
    start_time: datetime = None,
    end_time: datetime = None,
    limit: int = Query(default=100, le=1000)
):
    """
    Retrieve application logs
    
    Parameters:
    - level: Filter by log level (INFO, ERROR, etc.)
    - request_id: Filter by specific request ID
    - start_time: Filter logs from this time
    - end_time: Filter logs until this time
    - limit: Maximum number of logs to return (max 1000)
    """
    return await redis_logger.get_logs(
        level=level,
        request_id=request_id,
        start_time=start_time,
        end_time=end_time,
        limit=limit
    )
