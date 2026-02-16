"""
Repository pattern for database operations.

Provides clean abstraction over SQLAlchemy for CRUD operations.
"""

from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import desc

from viiper.core.project import Project, ProjectMetadata
from viiper.core.phase import Phase
from viiper.core.variant import Variant
from viiper.core.health import HealthScore, DimensionScore, HealthDimension
from viiper.agents.base import Agent, AgentRole, AgentCapability, AgentTask
from viiper.persistence.models import (
    ProjectModel,
    AgentModel,
    TaskModel,
    HealthScoreModel,
)


class ProjectRepository:
    """
    Repository for Project persistence operations.

    Handles conversion between Pydantic Project models and SQLAlchemy ProjectModel.
    """

    def __init__(self, session: Session):
        """
        Initialize repository with database session.

        Args:
            session: SQLAlchemy session
        """
        self.session = session

    def create(self, project: Project) -> Project:
        """
        Create a new project in the database.

        Args:
            project: Project to create

        Returns:
            Created project with database-generated fields
        """
        # Convert Pydantic to SQLAlchemy model
        db_project = self._to_db_model(project)

        # Add to session and commit
        self.session.add(db_project)
        self.session.commit()
        self.session.refresh(db_project)

        # Save current health score if exists
        if project.health_score:
            self._save_health_score(project.id, project.health_score)

        return self._from_db_model(db_project)

    def get(self, project_id: str) -> Optional[Project]:
        """
        Get project by ID.

        Args:
            project_id: Project ID

        Returns:
            Project if found, None otherwise
        """
        db_project = (
            self.session.query(ProjectModel).filter(ProjectModel.id == project_id).first()
        )

        if db_project is None:
            return None

        return self._from_db_model(db_project)

    def get_by_name(self, name: str) -> Optional[Project]:
        """
        Get project by name.

        Args:
            name: Project name

        Returns:
            Project if found, None otherwise
        """
        db_project = (
            self.session.query(ProjectModel).filter(ProjectModel.name == name).first()
        )

        if db_project is None:
            return None

        return self._from_db_model(db_project)

    def list(
        self,
        status: Optional[str] = None,
        variant: Optional[Variant] = None,
        phase: Optional[Phase] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Project]:
        """
        List projects with optional filters.

        Args:
            status: Filter by status
            variant: Filter by variant
            phase: Filter by phase
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            List of projects
        """
        query = self.session.query(ProjectModel)

        # Apply filters
        if status:
            query = query.filter(ProjectModel.status == status)
        if variant:
            query = query.filter(ProjectModel.variant == variant.value)
        if phase:
            query = query.filter(ProjectModel.phase == phase.value)

        # Order by most recently updated
        query = query.order_by(desc(ProjectModel.updated_at))

        # Apply pagination
        query = query.limit(limit).offset(offset)

        # Execute and convert
        db_projects = query.all()
        return [self._from_db_model(db_project) for db_project in db_projects]

    def update(self, project: Project) -> Project:
        """
        Update an existing project.

        Args:
            project: Project with updated fields

        Returns:
            Updated project
        """
        db_project = (
            self.session.query(ProjectModel).filter(ProjectModel.id == project.id).first()
        )

        if db_project is None:
            raise ValueError(f"Project with id {project.id} not found")

        # Update fields
        self._update_db_model(db_project, project)

        # Update timestamp
        db_project.updated_at = datetime.now()

        # Commit
        self.session.commit()
        self.session.refresh(db_project)

        # Save health score if updated
        if project.health_score:
            self._save_health_score(project.id, project.health_score)

        return self._from_db_model(db_project)

    def delete(self, project_id: str) -> bool:
        """
        Delete a project (soft delete by setting status to 'archived').

        Args:
            project_id: Project ID to delete

        Returns:
            True if deleted, False if not found
        """
        db_project = (
            self.session.query(ProjectModel).filter(ProjectModel.id == project_id).first()
        )

        if db_project is None:
            return False

        # Soft delete: set status to archived
        db_project.status = "archived"
        db_project.updated_at = datetime.now()

        self.session.commit()
        return True

    def hard_delete(self, project_id: str) -> bool:
        """
        Permanently delete a project from database.

        Args:
            project_id: Project ID to delete

        Returns:
            True if deleted, False if not found
        """
        db_project = (
            self.session.query(ProjectModel).filter(ProjectModel.id == project_id).first()
        )

        if db_project is None:
            return False

        self.session.delete(db_project)
        self.session.commit()
        return True

    def count(self, status: Optional[str] = None) -> int:
        """
        Count projects.

        Args:
            status: Optional status filter

        Returns:
            Number of projects
        """
        query = self.session.query(ProjectModel)

        if status:
            query = query.filter(ProjectModel.status == status)

        return query.count()

    def _to_db_model(self, project: Project) -> ProjectModel:
        """Convert Pydantic Project to SQLAlchemy ProjectModel."""
        return ProjectModel(
            id=project.id,
            name=project.name,
            variant=project.variant.value,
            phase=project.phase.value,
            status=project.status,
            created_at=project.created_at,
            updated_at=project.updated_at,
            started_at=project.started_at,
            timeline_weeks=project.timeline_weeks,
            budget=project.budget,
            budget_spent=project.budget_spent,
            target_users=project.target_users,
            target_revenue=project.target_revenue,
            current_users=project.current_users,
            current_revenue=project.current_revenue,
            metadata_tags=project.metadata.tags,
            metadata_industry=project.metadata.industry,
            metadata_target_market=project.metadata.target_market,
            metadata_tech_stack=project.metadata.tech_stack,
            metadata_notes=project.metadata.notes,
        )

    def _from_db_model(self, db_project: ProjectModel) -> Project:
        """Convert SQLAlchemy ProjectModel to Pydantic Project."""
        # Get latest health score if exists
        health_score = None
        if db_project.health_scores:
            latest_health = db_project.health_scores[0]  # Already ordered by desc
            health_score = HealthScore(
                performance=DimensionScore(
                    dimension=HealthDimension.PERFORMANCE,
                    score=latest_health.performance_score,
                    metrics=latest_health.performance_metrics or {},
                ),
                acquisition=DimensionScore(
                    dimension=HealthDimension.ACQUISITION,
                    score=latest_health.acquisition_score,
                    metrics=latest_health.acquisition_metrics or {},
                ),
                engagement=DimensionScore(
                    dimension=HealthDimension.ENGAGEMENT,
                    score=latest_health.engagement_score,
                    metrics=latest_health.engagement_metrics or {},
                ),
                revenue=DimensionScore(
                    dimension=HealthDimension.REVENUE,
                    score=latest_health.revenue_score,
                    metrics=latest_health.revenue_metrics or {},
                ),
            )

        return Project(
            id=db_project.id,
            name=db_project.name,
            variant=Variant(db_project.variant),
            phase=Phase(db_project.phase),
            status=db_project.status,
            created_at=db_project.created_at,
            updated_at=db_project.updated_at,
            started_at=db_project.started_at,
            timeline_weeks=db_project.timeline_weeks,
            budget=db_project.budget,
            budget_spent=db_project.budget_spent,
            target_users=db_project.target_users,
            target_revenue=db_project.target_revenue,
            current_users=db_project.current_users,
            current_revenue=db_project.current_revenue,
            health_score=health_score,
            metadata=ProjectMetadata(
                tags=db_project.metadata_tags or [],
                industry=db_project.metadata_industry,
                target_market=db_project.metadata_target_market,
                tech_stack=db_project.metadata_tech_stack or {},
                notes=db_project.metadata_notes,
            ),
        )

    def _update_db_model(self, db_project: ProjectModel, project: Project) -> None:
        """Update SQLAlchemy model with Pydantic model fields."""
        db_project.name = project.name
        db_project.variant = project.variant.value
        db_project.phase = project.phase.value
        db_project.status = project.status
        db_project.started_at = project.started_at
        db_project.timeline_weeks = project.timeline_weeks
        db_project.budget = project.budget
        db_project.budget_spent = project.budget_spent
        db_project.target_users = project.target_users
        db_project.target_revenue = project.target_revenue
        db_project.current_users = project.current_users
        db_project.current_revenue = project.current_revenue
        db_project.metadata_tags = project.metadata.tags
        db_project.metadata_industry = project.metadata.industry
        db_project.metadata_target_market = project.metadata.target_market
        db_project.metadata_tech_stack = project.metadata.tech_stack
        db_project.metadata_notes = project.metadata.notes

    def _save_health_score(self, project_id: str, health_score: HealthScore) -> None:
        """Save health score to database."""
        db_health = HealthScoreModel(
            project_id=project_id,
            overall_score=health_score.overall,
            performance_score=health_score.performance.score,
            performance_metrics=health_score.performance.metrics,
            acquisition_score=health_score.acquisition.score,
            acquisition_metrics=health_score.acquisition.metrics,
            engagement_score=health_score.engagement.score,
            engagement_metrics=health_score.engagement.metrics,
            revenue_score=health_score.revenue.score,
            revenue_metrics=health_score.revenue.metrics,
        )

        self.session.add(db_health)
        self.session.commit()


class AgentRepository:
    """
    Repository for Agent persistence operations.

    Handles conversion between Pydantic Agent models and SQLAlchemy AgentModel.
    """

    def __init__(self, session: Session):
        """
        Initialize repository with database session.

        Args:
            session: SQLAlchemy session
        """
        self.session = session

    def create(self, agent: Agent) -> Agent:
        """
        Create a new agent in the database.

        Args:
            agent: Agent to create

        Returns:
            Created agent
        """
        db_agent = AgentModel(
            id=agent.id,
            name=agent.name,
            role=agent.role.value,
            capabilities=[cap.value for cap in agent.capabilities],
            skills=agent.skills,
            status=agent.status,
            success_rate=agent.success_rate,
            total_tasks=agent.total_tasks,
            max_parallel_tasks=agent.max_parallel_tasks,
            auto_learn=agent.auto_learn,
        )

        self.session.add(db_agent)
        self.session.commit()
        self.session.refresh(db_agent)

        return agent

    def get(self, agent_id: str) -> Optional[AgentModel]:
        """
        Get agent by ID.

        Args:
            agent_id: Agent ID

        Returns:
            Agent model if found, None otherwise
        """
        return self.session.query(AgentModel).filter(AgentModel.id == agent_id).first()

    def list(
        self, role: Optional[AgentRole] = None, status: Optional[str] = None
    ) -> List[AgentModel]:
        """
        List agents with optional filters.

        Args:
            role: Filter by role
            status: Filter by status

        Returns:
            List of agent models
        """
        query = self.session.query(AgentModel)

        if role:
            query = query.filter(AgentModel.role == role.value)
        if status:
            query = query.filter(AgentModel.status == status)

        return query.all()

    def update(self, agent: Agent) -> bool:
        """
        Update an existing agent.

        Args:
            agent: Agent with updated fields

        Returns:
            True if updated, False if not found
        """
        db_agent = self.session.query(AgentModel).filter(AgentModel.id == agent.id).first()

        if db_agent is None:
            return False

        # Update fields
        db_agent.name = agent.name
        db_agent.status = agent.status
        db_agent.success_rate = agent.success_rate
        db_agent.total_tasks = agent.total_tasks
        db_agent.updated_at = datetime.now()

        self.session.commit()
        return True

    def delete(self, agent_id: str) -> bool:
        """
        Delete an agent from database.

        Args:
            agent_id: Agent ID to delete

        Returns:
            True if deleted, False if not found
        """
        db_agent = self.session.query(AgentModel).filter(AgentModel.id == agent_id).first()

        if db_agent is None:
            return False

        self.session.delete(db_agent)
        self.session.commit()
        return True
