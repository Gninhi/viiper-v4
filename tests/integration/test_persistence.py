"""
Integration tests for persistence layer.

Tests database models, repositories, and migrations.
"""

import pytest
from datetime import datetime, timedelta

from viiper.core.project import Project, ProjectMetadata
from viiper.core.phase import Phase
from viiper.core.variant import Variant
from viiper.core.health import HealthScore, DimensionScore, HealthDimension
from viiper.persistence import Database, ProjectRepository
from viiper.persistence.models import ProjectModel


@pytest.fixture
def db():
    """Create in-memory test database."""
    database = Database(database_url="sqlite:///:memory:", echo=False)
    database.create_tables()
    yield database
    database.drop_tables()


@pytest.fixture
def session(db):
    """Create database session for testing."""
    session = db.get_session()
    yield session
    session.close()


@pytest.fixture
def project_repo(session):
    """Create ProjectRepository for testing."""
    return ProjectRepository(session)


@pytest.fixture
def sample_project():
    """Create a sample project for testing."""
    return Project(
        name="Test SaaS",
        variant=Variant.SAAS,
        phase=Phase.VALIDATION,
        budget=10000.0,
        timeline_weeks=12,
        target_users=100,
        target_revenue=50000.0,
        current_users=25,
        current_revenue=5000.0,
        budget_spent=2500.0,
        started_at=datetime.now() - timedelta(weeks=2),
        metadata=ProjectMetadata(
            tags=["mvp", "ai"],
            industry="Tech",
            target_market="B2B SaaS",
            tech_stack={"frontend": "Next.js", "backend": "FastAPI"},
            notes="Test project for integration tests"
        )
    )


class TestDatabase:
    """Tests for Database class."""

    def test_database_creation(self):
        """Test creating database with tables."""
        db = Database(database_url="sqlite:///:memory:")
        db.create_tables()

        # Tables should be created
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        assert "projects" in tables
        assert "agents" in tables
        assert "tasks" in tables
        assert "health_scores" in tables

    def test_session_scope(self, db):
        """Test session scope context manager."""
        with db.session_scope() as session:
            # Should have a valid session
            assert session is not None
            assert session.is_active


class TestProjectRepository:
    """Tests for ProjectRepository."""

    def test_create_project(self, project_repo, sample_project):
        """Test creating a project."""
        created = project_repo.create(sample_project)

        assert created.id == sample_project.id
        assert created.name == sample_project.name
        assert created.variant == Variant.SAAS
        assert created.phase == Phase.VALIDATION
        assert created.budget == 10000.0
        assert created.timeline_weeks == 12

    def test_get_project_by_id(self, project_repo, sample_project):
        """Test retrieving project by ID."""
        # Create project
        created = project_repo.create(sample_project)

        # Retrieve by ID
        retrieved = project_repo.get(created.id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.name == created.name
        assert retrieved.variant == created.variant

    def test_get_project_by_name(self, project_repo, sample_project):
        """Test retrieving project by name."""
        # Create project
        created = project_repo.create(sample_project)

        # Retrieve by name
        retrieved = project_repo.get_by_name(created.name)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.name == created.name

    def test_get_nonexistent_project(self, project_repo):
        """Test getting a project that doesn't exist."""
        result = project_repo.get("nonexistent-id")
        assert result is None

    def test_list_projects(self, project_repo, sample_project):
        """Test listing projects."""
        # Create multiple projects
        project1 = project_repo.create(sample_project)

        project2 = Project(
            name="Test Landing",
            variant=Variant.LANDING,
            budget=2000.0,
            timeline_weeks=4
        )
        project_repo.create(project2)

        # List all projects
        projects = project_repo.list()
        assert len(projects) == 2

    def test_list_projects_with_filters(self, project_repo, sample_project):
        """Test listing projects with filters."""
        # Create projects with different variants
        project_repo.create(sample_project)

        project2 = Project(
            name="Test Landing",
            variant=Variant.LANDING,
            budget=2000.0,
            timeline_weeks=4
        )
        project_repo.create(project2)

        # Filter by variant
        saas_projects = project_repo.list(variant=Variant.SAAS)
        assert len(saas_projects) == 1
        assert saas_projects[0].variant == Variant.SAAS

        landing_projects = project_repo.list(variant=Variant.LANDING)
        assert len(landing_projects) == 1
        assert landing_projects[0].variant == Variant.LANDING

    def test_list_with_pagination(self, project_repo):
        """Test list with pagination."""
        # Create 5 projects
        for i in range(5):
            project = Project(
                name=f"Test Project {i}",
                variant=Variant.SAAS,
                budget=10000.0,
                timeline_weeks=12
            )
            project_repo.create(project)

        # Get first 3
        page1 = project_repo.list(limit=3, offset=0)
        assert len(page1) == 3

        # Get next 2
        page2 = project_repo.list(limit=3, offset=3)
        assert len(page2) == 2

    def test_update_project(self, project_repo, sample_project):
        """Test updating a project."""
        # Create project
        created = project_repo.create(sample_project)

        # Update fields
        created.name = "Updated Name"
        created.budget_spent = 5000.0
        created.current_users = 50
        created.phase = Phase.IDEATION

        # Save updates
        updated = project_repo.update(created)

        assert updated.name == "Updated Name"
        assert updated.budget_spent == 5000.0
        assert updated.current_users == 50
        assert updated.phase == Phase.IDEATION

    def test_update_nonexistent_project(self, project_repo, sample_project):
        """Test updating a project that doesn't exist."""
        # Create project but don't save it
        sample_project.id = "nonexistent-id"

        # Should raise error
        with pytest.raises(ValueError):
            project_repo.update(sample_project)

    def test_delete_project_soft(self, project_repo, sample_project):
        """Test soft deleting a project."""
        # Create project
        created = project_repo.create(sample_project)

        # Soft delete
        result = project_repo.delete(created.id)
        assert result is True

        # Project should exist but be archived
        retrieved = project_repo.get(created.id)
        assert retrieved is not None
        assert retrieved.status == "archived"

    def test_delete_project_hard(self, project_repo, sample_project):
        """Test hard deleting a project."""
        # Create project
        created = project_repo.create(sample_project)

        # Hard delete
        result = project_repo.hard_delete(created.id)
        assert result is True

        # Project should not exist
        retrieved = project_repo.get(created.id)
        assert retrieved is None

    def test_delete_nonexistent_project(self, project_repo):
        """Test deleting a project that doesn't exist."""
        result = project_repo.delete("nonexistent-id")
        assert result is False

    def test_count_projects(self, project_repo, sample_project):
        """Test counting projects."""
        # Initially 0
        count = project_repo.count()
        assert count == 0

        # Create project
        project_repo.create(sample_project)

        # Should be 1
        count = project_repo.count()
        assert count == 1

        # Create another
        project2 = Project(
            name="Test Landing",
            variant=Variant.LANDING,
            budget=2000.0,
            timeline_weeks=4
        )
        project_repo.create(project2)

        # Should be 2
        count = project_repo.count()
        assert count == 2

    def test_count_with_filter(self, project_repo, sample_project):
        """Test counting projects with status filter."""
        # Create active project
        project_repo.create(sample_project)

        # Create and archive another
        project2 = Project(
            name="Test Landing",
            variant=Variant.LANDING,
            budget=2000.0,
            timeline_weeks=4
        )
        created2 = project_repo.create(project2)
        project_repo.delete(created2.id)  # Soft delete = archived

        # Count active
        active_count = project_repo.count(status="active")
        assert active_count == 1

        # Count archived
        archived_count = project_repo.count(status="archived")
        assert archived_count == 1

    def test_project_metadata_persistence(self, project_repo, sample_project):
        """Test that project metadata is persisted correctly."""
        # Create project with metadata
        created = project_repo.create(sample_project)

        # Retrieve and check metadata
        retrieved = project_repo.get(created.id)

        assert retrieved.metadata.tags == ["mvp", "ai"]
        assert retrieved.metadata.industry == "Tech"
        assert retrieved.metadata.target_market == "B2B SaaS"
        assert retrieved.metadata.tech_stack == {"frontend": "Next.js", "backend": "FastAPI"}
        assert retrieved.metadata.notes == "Test project for integration tests"

    def test_health_score_persistence(self, project_repo, sample_project):
        """Test that health scores are persisted correctly."""
        # Calculate and set health score
        sample_project.calculate_health_score()

        # Create project
        created = project_repo.create(sample_project)

        # Retrieve and check health score
        retrieved = project_repo.get(created.id)

        assert retrieved.health_score is not None
        assert retrieved.health_score.overall > 0
        assert retrieved.health_score.performance is not None
        assert retrieved.health_score.acquisition is not None
        assert retrieved.health_score.engagement is not None
        assert retrieved.health_score.revenue is not None

    def test_timeline_calculations(self, project_repo, sample_project):
        """Test that timeline calculations work after persistence."""
        # Create project
        created = project_repo.create(sample_project)

        # Retrieve and test calculations
        retrieved = project_repo.get(created.id)

        # Should have timeline progress (started 2 weeks ago, 12 week timeline)
        progress = retrieved.get_timeline_progress()
        assert 0.1 <= progress <= 0.2  # Approximately 2/12

        # Should have budget usage
        budget_usage = retrieved.get_budget_usage()
        assert budget_usage == 0.25  # 2500/10000

    def test_project_summary_after_persistence(self, project_repo, sample_project):
        """Test that project summary works after loading from database."""
        # Create project
        created = project_repo.create(sample_project)

        # Retrieve and get summary
        retrieved = project_repo.get(created.id)
        summary = retrieved.get_summary()

        assert summary["name"] == "Test SaaS"
        assert summary["variant"] == "SaaS Application"
        assert summary["phase"] == "Validation"
        assert "budget" in summary
        assert "timeline" in summary
        assert "metrics" in summary
