1. Create logger.py in backend/app/core/

Python
# backend/app/core/logger.py
import logging
import sys

def setup_logger(name):
    """
    Set up a logger with the specified name.

    Args:
        name: The name of the logger (typically __name__).

    Returns:
        A configured logger instance.
    """

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    handler = logging.StreamHandler(sys.stdout)  # Log to console
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set the desired logging level
    logger.addHandler(handler)

    return logger
2. Modify backend/app/core/config.py

Python
# backend/app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from core.logger import setup_logger  # Import the setup_logger function

# Set the logger for the current module
logger = setup_logger(__name__)

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False  # Default to False
    api_version_string: str = "/api/v1"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

# Example of using the logger in config.py
logger.debug(f"Debug mode is set to: {settings.debug}")
3. Use the Logger in Other Modules

Python
# backend/app/main.py
from fastapi import FastAPI
from core.config import settings
from core.logger import setup_logger  # Import setup_logger
from api.v1 import users, items

# Get a logger instance for this module
logger = setup_logger(__name__)

app = FastAPI(
    title="My Web App",
    description="A web application built with FastAPI and Vue.js",
    version="0.1.0",
    openapi_url=f"{settings.api_version_string}/openapi.json"
)

app.include_router(users.router, prefix=settings.api_version_string)
app.include_router(items.router, prefix=settings.api_version_string)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello World"}
Python
# backend/app/api/v1/users.py
from fastapi import APIRouter, HTTPException
from core.logger import setup_logger  # Import setup_logger

# Get a logger instance for this module
logger = setup_logger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/")
async def read_users():
    logger.info("Reading all users")  # Example log message
    return [{"username": "user1"}, {"username": "user2"}]

@router.get("/{user_id}")
async def read_user(user_id: int):
    logger.debug(f"Reading user with ID: {user_id}")  # Debug level log
    if user_id == 0:
        logger.warning("User ID 0 might be invalid")  # Warning level log
    if user_id > 100:
        logger.error(f"User ID {user_id} not found")  # Error level log
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id}
Explanation:

logger.py:

setup_logger(name):
Takes the module name (__name__) as input.
Creates a logging.Formatter to define the log message format (timestamp, logger name, level, message).
Creates a logging.StreamHandler to output logs to the console (you can add other handlers for file logging, etc.).
Sets the formatter for the handler.
Gets a logging.Logger instance with the given name.
Sets the logging level to logging.DEBUG (you can change this to INFO, WARNING, ERROR, etc.).
Adds the handler to the logger.
Returns the configured logger.
config.py:

The setup_logger function is imported and the logger is set for the config module.
Other Modules (e.g., main.py, users.py):

Import the setup_logger function from core.logger.
Call setup_logger(__name__) to get a logger instance specific to that module. The __name__ variable will automatically contain the correct module name (e.g., "app.api.v1.users").
Use the logger instance to log messages at different levels:
logger.debug(): For detailed debugging information.
logger.info(): For general informational messages.
logger.warning(): For potential issues or warnings.
logger.error(): For error conditions.
logger.critical(): For critical errors that might cause the application to fail.
Benefits of This Approach:

Centralized Configuration: You configure the logger's format, handlers, and level in one place (logger.py).
Module-Specific Names: Each module gets its own logger with a name that reflects its location in the project (e.g., app.api.v1.users). This makes it easier to trace where log messages are coming from.
Consistent Logging: All modules use the same logging setup, ensuring consistency across your application.
Flexibility: You can easily add more handlers (e.g., file handlers, email handlers), change the logging level, or modify the log format without changing code in every module.
Running the Application:

When you run your FastAPI application (e.g., using uvicorn app.main:app --reload), you'll see log messages in your console with the format you defined:

2023-10-27 10:30:00,000 - app.core.config - DEBUG - Debug mode is set to: True
2023-10-27 10:30:00,123 - app.main - INFO - Application startup
2023-10-27 10:30:05,456 - app.main - INFO - Root endpoint accessed
2023-10-27 10:30:10,789 - app.api.v1.users - INFO - Reading all users
2023-10-27 10:30:15,234 - app.api.v1.users - DEBUG - Reading user with ID: 5
2023-10-27 10:30:20,567 - app.api.v1.users - WARNING - User ID 0 might be invalid
2023-10-27 10:30:25,890 - app.api.v1.users - ERROR - User ID 105 not found
This setup provides a robust and maintainable logging system for your FastAPI backend! You can further customize it based on your specific requirements, such as adding file logging, integrating with log management systems, or using different logging levels for different environments (e.g., DEBUG in development, INFO in production).