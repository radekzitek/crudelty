from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings
from .logger import setup_logger

logger = setup_logger(__name__)
settings = get_settings()

logger.debug(f"Database URL: {settings.DATABASE_URL}")
# Create SQLAlchemy engine
try:
    engine = create_engine(
        settings.DATABASE_URL,
    )
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")
    raise

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

def get_db():
    """
    Database dependency to be used in FastAPI endpoints.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        logger.debug("Creating new database session")
        yield db
    finally:
        logger.debug("Closing database session")
        db.close()

def init_db():
    """
    Initialize database by creating all tables.
    Should be called when application starts.
    """
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Test connection
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        logger.info("Database connection test successful")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise 