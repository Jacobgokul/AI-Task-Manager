"""Database configuration and session management."""
import logging
from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from omegaconf import DictConfig

logger = logging.getLogger(__name__)

# Create declarative base for models
Base = declarative_base()

# Global variables for database engine and session
_engine: Optional[object] = None
_SessionLocal: Optional[sessionmaker] = None


def init_database(config: DictConfig) -> None:
    """
    Initialize database engine and session factory.

    Args:
        config: Hydra configuration object containing database settings

    Raises:
        ValueError: If database configuration is invalid
        Exception: If database connection fails
    """
    global _engine, _SessionLocal

    try:
        # Extract database configuration
        db_config = config.db

        # Build database URL
        database_url = (
            f"postgresql://{db_config.user}:{db_config.password}"
            f"@{db_config.host}:{db_config.port}/{db_config.database}"
        )

        logger.info(f"Initializing database connection to {db_config.host}:{db_config.port}")

        # Create engine with connection pooling
        _engine = create_engine(
            database_url,
            pool_pre_ping=True,  # Verify connections before using them
            pool_size=10,  # Maximum number of connections in the pool
            max_overflow=20,  # Maximum overflow connections beyond pool_size
            echo=db_config.get("echo", False),  # Log SQL statements if enabled
        )

        # Create session factory
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=_engine
        )

        logger.info("Database initialized successfully")

    except KeyError as e:
        error_msg = f"Missing database configuration key: {e}"
        logger.error(error_msg)
        raise ValueError(error_msg) from e
    except Exception as e:
        error_msg = f"Failed to initialize database: {e}"
        logger.error(error_msg)
        raise


def create_tables() -> None:
    """
    Create all database tables defined in models.

    Raises:
        RuntimeError: If database is not initialized
    """
    if _engine is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")

    try:
        logger.info("Creating database tables")
        Base.metadata.create_all(bind=_engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        error_msg = f"Failed to create database tables: {e}"
        logger.error(error_msg)
        raise


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.

    Yields:
        Session: SQLAlchemy database session

    Raises:
        RuntimeError: If database is not initialized
    """
    if _SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")

    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_engine() -> object:
    """
    Get the database engine instance.

    Returns:
        Engine: SQLAlchemy engine instance

    Raises:
        RuntimeError: If database is not initialized
    """
    if _engine is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    return _engine


def close_database() -> None:
    """Close database connections and cleanup resources."""
    global _engine, _SessionLocal

    if _engine is not None:
        logger.info("Closing database connections")
        _engine.dispose()
        _engine = None
        _SessionLocal = None
        logger.info("Database connections closed")
