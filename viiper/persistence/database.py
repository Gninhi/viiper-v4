"""
Database connection and session management.

Provides SQLAlchemy setup with connection pooling and session management.
"""

import os
from typing import Generator
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Base class for all models
Base = declarative_base()


class Database:
    """
    Database connection manager.

    Handles SQLAlchemy engine creation, session management,
    and database initialization.
    """

    def __init__(self, database_url: str | None = None, echo: bool = False):
        """
        Initialize database connection.

        Args:
            database_url: Database URL (defaults to SQLite in ~/.viiper/viiper.db)
            echo: Whether to echo SQL statements
        """
        if database_url is None:
            # Default: SQLite in user's home directory
            viiper_dir = Path.home() / ".viiper"
            viiper_dir.mkdir(exist_ok=True)
            db_path = viiper_dir / "viiper.db"
            database_url = f"sqlite:///{db_path}"

        self.database_url = database_url
        self.echo = echo

        # Create engine
        if database_url.startswith("sqlite"):
            # SQLite-specific configuration
            self.engine = create_engine(
                database_url,
                echo=echo,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,  # Use StaticPool for SQLite
            )

            # Enable foreign keys for SQLite
            @event.listens_for(self.engine, "connect")
            def set_sqlite_pragma(dbapi_conn, connection_record):
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
        else:
            # PostgreSQL or other databases
            self.engine = create_engine(
                database_url,
                echo=echo,
                pool_pre_ping=True,  # Verify connections before using
                pool_size=5,
                max_overflow=10,
            )

        # Create session factory
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )

    def create_tables(self) -> None:
        """Create all tables in the database."""
        Base.metadata.create_all(bind=self.engine)

    def drop_tables(self) -> None:
        """Drop all tables (use with caution!)."""
        Base.metadata.drop_all(bind=self.engine)

    def get_session(self) -> Session:
        """
        Get a new database session.

        Returns:
            SQLAlchemy session
        """
        return self.SessionLocal()

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
        Context manager for database sessions with automatic commit/rollback.

        Usage:
            with db.session_scope() as session:
                session.add(model)
                # Automatically commits on success, rolls back on error

        Yields:
            Database session
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


# Global database instance
_db_instance: Database | None = None


def get_database(database_url: str | None = None, echo: bool = False) -> Database:
    """
    Get or create the global database instance.

    Args:
        database_url: Database URL (only used on first call)
        echo: Whether to echo SQL (only used on first call)

    Returns:
        Database instance
    """
    global _db_instance

    if _db_instance is None:
        _db_instance = Database(database_url=database_url, echo=echo)

    return _db_instance


def get_session() -> Session:
    """
    Get a new database session from the global database instance.

    Returns:
        SQLAlchemy session
    """
    db = get_database()
    return db.get_session()


def init_database(database_url: str | None = None, echo: bool = False) -> Database:
    """
    Initialize the database and create all tables.

    Args:
        database_url: Database URL
        echo: Whether to echo SQL

    Returns:
        Database instance
    """
    db = get_database(database_url=database_url, echo=echo)
    db.create_tables()
    return db
