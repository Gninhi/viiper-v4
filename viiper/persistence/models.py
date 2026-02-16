"""
SQLAlchemy database models for VIIPER.

Maps Pydantic domain models to database tables.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    JSON,
    Index,
)
from sqlalchemy.orm import relationship

from viiper.persistence.database import Base


class ProjectModel(Base):
    """
    Database model for VIIPER projects.

    Stores project metadata, state, budget, timeline, and health information.
    """

    __tablename__ = "projects"

    # Primary key
    id = Column(String(36), primary_key=True, index=True)

    # Identity
    name = Column(String(255), nullable=False, index=True)
    variant = Column(String(50), nullable=False, index=True)

    # State
    phase = Column(String(50), nullable=False, default="validation", index=True)
    status = Column(String(50), nullable=False, default="active", index=True)

    # Timeline
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    started_at = Column(DateTime, nullable=True)
    timeline_weeks = Column(Integer, nullable=False)

    # Budget
    budget = Column(Float, nullable=False)
    budget_spent = Column(Float, nullable=False, default=0.0)

    # Goals & Metrics
    target_users = Column(Integer, nullable=True)
    target_revenue = Column(Float, nullable=True)
    current_users = Column(Integer, nullable=False, default=0)
    current_revenue = Column(Float, nullable=False, default=0.0)

    # Metadata (stored as JSON)
    metadata_tags = Column(JSON, nullable=True)
    metadata_industry = Column(String(255), nullable=True)
    metadata_target_market = Column(String(255), nullable=True)
    metadata_tech_stack = Column(JSON, nullable=True)
    metadata_notes = Column(Text, nullable=True)

    # Relationships
    health_scores = relationship(
        "HealthScoreModel",
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="desc(HealthScoreModel.created_at)",
    )
    tasks = relationship(
        "TaskModel",
        back_populates="project",
        cascade="all, delete-orphan",
    )

    # Indexes for common queries
    __table_args__ = (
        Index("idx_project_status_phase", "status", "phase"),
        Index("idx_project_created", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<ProjectModel(id={self.id}, name={self.name}, variant={self.variant})>"


class AgentModel(Base):
    """
    Database model for VIIPER agents.

    Stores agent configuration, state, and performance metrics.
    """

    __tablename__ = "agents"

    # Primary key
    id = Column(String(36), primary_key=True, index=True)

    # Identity
    name = Column(String(255), nullable=False, index=True)
    role = Column(String(50), nullable=False, index=True)

    # Capabilities (stored as JSON array)
    capabilities = Column(JSON, nullable=False)
    skills = Column(JSON, nullable=False)

    # State
    status = Column(String(50), nullable=False, default="idle", index=True)

    # Performance
    success_rate = Column(Float, nullable=False, default=1.0)
    total_tasks = Column(Integer, nullable=False, default=0)

    # Configuration
    max_parallel_tasks = Column(Integer, nullable=False, default=1)
    auto_learn = Column(Boolean, nullable=False, default=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Relationships
    tasks = relationship(
        "TaskModel",
        back_populates="agent",
        foreign_keys="TaskModel.agent_id",
    )

    def __repr__(self) -> str:
        return f"<AgentModel(id={self.id}, name={self.name}, role={self.role})>"


class TaskModel(Base):
    """
    Database model for agent tasks.

    Stores task details, assignment, status, and results.
    """

    __tablename__ = "tasks"

    # Primary key
    id = Column(String(36), primary_key=True, index=True)

    # Task details
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    priority = Column(Integer, nullable=False, default=5)
    status = Column(String(50), nullable=False, default="pending", index=True)

    # Assignment
    agent_id = Column(String(36), ForeignKey("agents.id"), nullable=True, index=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=True, index=True)

    # Results
    result = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    agent = relationship("AgentModel", back_populates="tasks", foreign_keys=[agent_id])
    project = relationship("ProjectModel", back_populates="tasks")

    # Indexes
    __table_args__ = (
        Index("idx_task_status_priority", "status", "priority"),
        Index("idx_task_agent_status", "agent_id", "status"),
    )

    def __repr__(self) -> str:
        return f"<TaskModel(id={self.id}, name={self.name}, status={self.status})>"


class HealthScoreModel(Base):
    """
    Database model for project health scores.

    Stores health metrics across four dimensions: Performance, Acquisition,
    Engagement, and Revenue.
    """

    __tablename__ = "health_scores"

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign key
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False, index=True)

    # Overall score
    overall_score = Column(Float, nullable=False)

    # Dimension scores
    performance_score = Column(Float, nullable=False)
    performance_metrics = Column(JSON, nullable=True)

    acquisition_score = Column(Float, nullable=False)
    acquisition_metrics = Column(JSON, nullable=True)

    engagement_score = Column(Float, nullable=False)
    engagement_metrics = Column(JSON, nullable=True)

    revenue_score = Column(Float, nullable=False)
    revenue_metrics = Column(JSON, nullable=True)

    # Timestamp
    created_at = Column(DateTime, nullable=False, default=datetime.now, index=True)

    # Relationships
    project = relationship("ProjectModel", back_populates="health_scores")

    # Indexes
    __table_args__ = (Index("idx_health_project_created", "project_id", "created_at"),)

    def __repr__(self) -> str:
        return f"<HealthScoreModel(project_id={self.project_id}, overall={self.overall_score:.1f})>"
