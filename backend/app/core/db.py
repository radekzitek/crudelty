from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from urllib.parse import urlparse
from contextlib import contextmanager
from .config import get_settings
from .logger import setup_logger

logger = setup_logger(__name__)
settings = get_settings()

# Parse and log database URL components safely (without password)
try:
    db_url = urlparse(settings.DATABASE_URL)
    logger.debug("Database connection details:")
    logger.debug(f"  - Driver: {db_url.scheme}")
    logger.debug(f"  - Host: {db_url.hostname}")
    logger.debug(f"  - Port: {db_url.port}")
    logger.debug(f"  - Database: {db_url.path[1:] if db_url.path else 'None'}")
    logger.debug(f"  - Username: {db_url.username}")
except Exception as e:
    logger.error(f"Error parsing DATABASE_URL: {str(e)}")

# Modify URL to use PyMySQL
mysql_url = settings.DATABASE_URL.replace('mysql://', 'mysql+pymysql://')

# Create SQLAlchemy engine
try:
    engine = create_engine(
        mysql_url,
        poolclass=QueuePool,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_timeout=settings.DB_POOL_TIMEOUT,
        pool_recycle=settings.DB_POOL_RECYCLE,
        pool_pre_ping=True,
        echo=settings.DEBUG,
        echo_pool=settings.DEBUG
    )
    logger.info("Database engine created successfully")
    
    # Test connection and get version
    with engine.connect() as conn:
        version = conn.execute(text("SELECT VERSION()")).scalar()
        logger.info(f"Connected to MySQL version: {version}")
        
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")
    raise

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()

@contextmanager
def get_db():
    """
    Context manager for database sessions.
    Usage:
        with get_db() as db:
            db.query(Model).all()
    """
    db = SessionLocal()
    try:
        logger.debug("Creating new database session")
        yield db
        db.commit()
        logger.debug("Session committed successfully")
    except Exception as e:
        db.rollback()
        logger.error(f"Session rollback due to error: {str(e)}")
        raise
    finally:
        logger.debug("Closing database session")
        db.close()

def get_db_session():
    """
    Dependency for FastAPI endpoints.
    Usage:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db_session)):
            return db.query(Model).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_info():
    """Get database structure information"""
    try:
        with engine.connect() as conn:
            # Get current database
            db_name = conn.execute(text("SELECT DATABASE()")).scalar()
            logger.info(f"Current database: {db_name}")
            
            # Get tables
            tables = conn.execute(text("""
                SELECT TABLE_NAME, ENGINE, TABLE_ROWS, CREATE_TIME
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = :db
                ORDER BY TABLE_NAME
            """), {"db": db_name}).fetchall()
            
            logger.info(f"Found {len(tables)} tables:")
            for table in tables:
                logger.info(f"\nTable: {table.TABLE_NAME}")
                logger.info(f"  Engine: {table.ENGINE}")
                logger.info(f"  Rows (approximate): {table.TABLE_ROWS}")
                logger.info(f"  Created: {table.CREATE_TIME}")
                
                # Get columns
                columns = conn.execute(text("""
                    SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY, EXTRA
                    FROM information_schema.COLUMNS
                    WHERE TABLE_SCHEMA = :db AND TABLE_NAME = :table
                    ORDER BY ORDINAL_POSITION
                """), {"db": db_name, "table": table.TABLE_NAME}).fetchall()
                
                logger.info("  Columns:")
                for col in columns:
                    nullable = "NULL" if col.IS_NULLABLE == "YES" else "NOT NULL"
                    key = f", {col.COLUMN_KEY}" if col.COLUMN_KEY else ""
                    extra = f", {col.EXTRA}" if col.EXTRA else ""
                    logger.info(f"    - {col.COLUMN_NAME}: {col.COLUMN_TYPE} {nullable}{key}{extra}")
                
                # Get indexes
                indexes = conn.execute(text("""
                    SELECT INDEX_NAME, COLUMN_NAME, NON_UNIQUE
                    FROM information_schema.STATISTICS
                    WHERE TABLE_SCHEMA = :db AND TABLE_NAME = :table
                    ORDER BY INDEX_NAME, SEQ_IN_INDEX
                """), {"db": db_name, "table": table.TABLE_NAME}).fetchall()
                
                if indexes:
                    logger.info("  Indexes:")
                    current_index = None
                    columns = []
                    for idx in indexes:
                        if current_index != idx.INDEX_NAME:
                            if current_index:
                                unique = "UNIQUE " if not indexes[0].NON_UNIQUE else ""
                                logger.info(f"    - {unique}{current_index}: {', '.join(columns)}")
                                columns = []
                            current_index = idx.INDEX_NAME
                        columns.append(idx.COLUMN_NAME)
                    if columns:
                        unique = "UNIQUE " if not indexes[-1].NON_UNIQUE else ""
                        logger.info(f"    - {unique}{current_index}: {', '.join(columns)}")
                
                # Get foreign keys
                foreign_keys = conn.execute(text("""
                    SELECT CONSTRAINT_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
                    FROM information_schema.KEY_COLUMN_USAGE
                    WHERE TABLE_SCHEMA = :db AND TABLE_NAME = :table
                        AND REFERENCED_TABLE_NAME IS NOT NULL
                    ORDER BY CONSTRAINT_NAME
                """), {"db": db_name, "table": table.TABLE_NAME}).fetchall()
                
                if foreign_keys:
                    logger.info("  Foreign Keys:")
                    for fk in foreign_keys:
                        logger.info(f"    - {fk.CONSTRAINT_NAME}: {fk.COLUMN_NAME} -> {fk.REFERENCED_TABLE_NAME}.{fk.REFERENCED_COLUMN_NAME}")
            
            return True
            
    except Exception as e:
        logger.error(f"Error getting database information: {str(e)}")
        return False

async def check_db_health(db_session) -> tuple[bool, str]:
    """Check database connectivity and return status"""
    try:
        # Get database version
        result = await db_session.execute(text("SELECT VERSION()"))
        version = result.scalar()
        await db_session.commit()
        return True, f"Connected to MySQL version: {version}"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False, f"Database error: {str(e)}"

# Export commonly used database components
__all__ = ['engine', 'Base', 'get_db', 'get_db_session', 'get_db_info'] 