"""
Database models and session management
"""

from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from src.config import config

# Create database engine
engine = create_engine(
    config.database.url,
    echo=config.database.echo,
    connect_args={"check_same_thread": False} if "sqlite" in config.database.url else {},
    pool_size=config.database.pool_size,
    max_overflow=config.database.max_overflow,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


class ScrapedData(Base):
    """Model for storing scraped data"""

    __tablename__ = "scraped_data"

    id = Column(Integer, primary_key=True, index=True)
    source_url = Column(String, nullable=False, index=True)
    data_type = Column(String, nullable=False)  # e.g., "html", "json", "text"
    raw_data = Column(Text, nullable=False)
    processed_data = Column(Text, nullable=True)
    scraped_at = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<ScrapedData(id={self.id}, source_url={self.source_url})>"


class WorkflowRun(Base):
    """Model for storing workflow execution history"""

    __tablename__ = "workflow_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String, unique=True, nullable=False, index=True)
    workflow_name = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False)  # pending, running, success, failed
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=True)  # seconds
    tasks_run = Column(Integer, default=0)
    tasks_failed = Column(Integer, default=0)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<WorkflowRun(id={self.id}, workflow_name={self.workflow_name}, status={self.status})>"


def get_session() -> Session:
    """Get database session"""
    return SessionLocal()


def init_db() -> None:
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """Drop all database tables (development only)"""
    Base.metadata.drop_all(bind=engine)


if __name__ == "__main__":
    # Initialize database
    init_db()
    print("Database initialized successfully!")
