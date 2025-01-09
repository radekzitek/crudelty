# backend/app/app.py
from fastapi import FastAPI
from .core.logger import setup_logger
from .core.config import get_settings
from .api.v1 import api_router

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

# Include API router with version prefix
app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX
)

@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
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
