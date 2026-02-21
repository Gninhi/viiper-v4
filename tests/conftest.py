"""
Pytest configuration and shared fixtures for VIIPER tests.

This module provides common fixtures used across all test modules.
"""

import pytest
from datetime import datetime, timedelta

# Core imports
from viiper.core.project import Project, ProjectMetadata
from viiper.core.phase import Phase
from viiper.core.variant import Variant
from viiper.core.health import HealthScore, DimensionScore, HealthDimension

# Persistence imports
from viiper.persistence import Database, ProjectRepository, AgentRepository
from viiper.persistence.models import ProjectModel, AgentModel, TaskModel

# Agent imports
from viiper.agents.base import Agent, AgentRole, AgentCapability, AgentTask
from viiper.agents.factory import AgentFactory

# Skills imports
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty


# =============================================================================
# DATABASE FIXTURES
# =============================================================================


@pytest.fixture(scope="function")
def db():
    """Create in-memory test database.

    Yields:
        Database: Test database instance
    """
    database = Database(database_url="sqlite:///:memory:", echo=False)
    database.create_tables()
    yield database
    database.drop_tables()


@pytest.fixture(scope="function")
def session(db):
    """Create database session for testing.

    Yields:
        Session: SQLAlchemy session
    """
    session = db.get_session()
    yield session
    session.close()


# =============================================================================
# REPOSITORY FIXTURES
# =============================================================================


@pytest.fixture
def project_repo(session):
    """Create ProjectRepository for testing.

    Returns:
        ProjectRepository: Repository instance
    """
    return ProjectRepository(session)


@pytest.fixture
def agent_repo(session):
    """Create AgentRepository for testing.

    Returns:
        AgentRepository: Repository instance
    """
    return AgentRepository(session)


# =============================================================================
# PROJECT FIXTURES
# =============================================================================


@pytest.fixture
def sample_project():
    """Create a sample SaaS project for testing.

    Returns:
        Project: Sample project instance
    """
    return Project(
        name="Test SaaS",
        variant=Variant.SAAS,
        phase=Phase.VALIDATION,
        budget=10000.0,
        timeline_weeks=12,
        target_users=100,
        target_revenue=50000.0,
        metadata=ProjectMetadata(
            tags=["test", "saas"],
            industry="Technology",
            target_market="B2B",
        ),
    )


@pytest.fixture
def sample_landing_project():
    """Create a sample landing page project for testing.

    Returns:
        Project: Sample landing project instance
    """
    return Project(
        name="Test Landing Page",
        variant=Variant.LANDING,
        phase=Phase.IDEATION,
        budget=2000.0,
        timeline_weeks=4,
        target_users=1000,
        metadata=ProjectMetadata(
            tags=["test", "landing"],
            industry="Marketing",
        ),
    )


@pytest.fixture
def project_with_health():
    """Create a project with health score for testing.

    Returns:
        Project: Project with calculated health score
    """
    project = Project(
        name="Health Test Project",
        variant=Variant.SAAS,
        phase=Phase.PRODUCTION,
        budget=15000.0,
        budget_spent=5000.0,
        timeline_weeks=16,
        target_users=200,
        current_users=50,
        target_revenue=75000.0,
        current_revenue=10000.0,
    )
    # Calculate health score
    project.calculate_health_score()
    return project


# =============================================================================
# AGENT FIXTURES
# =============================================================================


@pytest.fixture
def sample_agent():
    """Create a sample agent for testing.

    Returns:
        Agent: Sample agent instance
    """
    from viiper.agents.research import MarketResearchAgent

    return MarketResearchAgent()


@pytest.fixture
def agent_factory():
    """Provide AgentFactory for testing.

    Returns:
        AgentFactory: Factory class
    """
    return AgentFactory


@pytest.fixture
def sample_task():
    """Create a sample agent task for testing.

    Returns:
        AgentTask: Sample task instance
    """
    return AgentTask(
        name="Test Task",
        description="A sample task for testing",
        priority=5,
    )


# =============================================================================
# SKILLS FIXTURES
# =============================================================================


@pytest.fixture
def sample_skill_metadata():
    """Create sample skill metadata for testing.

    Returns:
        SkillMetadata: Sample metadata instance
    """
    return SkillMetadata(
        name="Test Skill",
        slug="test-skill",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["test", "react"],
        estimated_time_minutes=30,
        description="A test skill for testing purposes",
    )


@pytest.fixture
def mock_skill_class():
    """Provide a mock skill class for testing.

    Returns:
        type: Mock skill class
    """

    class MockSkill(Skill):
        metadata: SkillMetadata = SkillMetadata(
            name="Mock Skill",
            slug="mock-skill",
            category=SkillCategory.FRONTEND_COMPONENTS,
            difficulty=SkillDifficulty.BEGINNER,
            description="A mock skill for testing",
        )

        def generate(self, context=None):
            return {"test.tsx": "export const Test = () => <div>Test</div>;"}

    return MockSkill


# =============================================================================
# HEALTH SCORE FIXTURES
# =============================================================================


@pytest.fixture
def sample_health_score():
    """Create a sample health score for testing.

    Returns:
        HealthScore: Sample health score instance
    """
    return HealthScore(
        performance=DimensionScore(
            dimension=HealthDimension.PERFORMANCE,
            score=8.5,
            metrics={"test_coverage": 0.85, "load_time": 1.2},
        ),
        acquisition=DimensionScore(
            dimension=HealthDimension.ACQUISITION,
            score=7.0,
            metrics={"user_growth": 0.15, "activation_rate": 0.65},
        ),
        engagement=DimensionScore(
            dimension=HealthDimension.ENGAGEMENT,
            score=6.5,
            metrics={"retention": 0.45, "session_duration": 300},
        ),
        revenue=DimensionScore(
            dimension=HealthDimension.REVENUE, score=5.0, metrics={"mrr": 5000, "cac": 50}
        ),
    )


# =============================================================================
# UTILITY FIXTURES
# =============================================================================


@pytest.fixture
def temp_dir(tmp_path):
    """Provide a temporary directory for testing.

    Args:
        tmp_path: Pytest built-in fixture

    Returns:
        Path: Temporary directory path
    """
    return tmp_path


@pytest.fixture
def mock_datetime():
    """Provide a mock datetime for consistent testing.

    Returns:
        datetime: Fixed datetime instance
    """
    return datetime(2026, 2, 18, 12, 0, 0)


# =============================================================================
# CONFIGURATION
# =============================================================================


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Mark tests in integration folder
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        # Mark tests in unit folder
        elif "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
