"""
Unit tests for Sprint 1.4: Backend Skills and Agent Integration (Fixed).
"""

import pytest
import asyncio
from typing import Dict, Any
from viiper.skills.backend.search_filtering import SearchFilteringSkill
from viiper.skills.backend.data_export import DataExportSkill
from viiper.skills.backend.migrations import MigrationsSkill
from viiper.skills.backend.testing_patterns import TestingPatternsSkill
from viiper.agents.factory import AgentFactory
from viiper.agents.base import AgentTask, AgentRole, AgentCapability
from viiper.agents.collaboration import CollaborationProtocol, MessageType, STANDARD_WORKFLOWS

class TestBackendSkills:
    """Tests for the new backend skills implemented in Sprint 1.4."""

    def test_search_filtering_skill(self):
        skill = SearchFilteringSkill()
        assert skill.metadata.slug == "search-filtering"
        code = skill.generate()
        assert "backend/lib/search.ts" in code
        assert "buildSearchQuery" in code["backend/lib/search.ts"]

    def test_data_export_skill(self):
        skill = DataExportSkill()
        assert "csv" in skill.metadata.tags
        code = skill.generate()
        assert "backend/lib/export_service.ts" in code
        assert "ExportService" in code["backend/lib/export_service.ts"]

    def test_migrations_skill(self):
        skill = MigrationsSkill()
        assert skill.metadata.category.value == "backend_database"
        code = skill.generate()
        assert "prisma/schema.prisma" in code
        assert "alembic" in skill.get_documentation()

    def test_testing_patterns_skill_metadata(self):
        skill = TestingPatternsSkill()
        assert "pytest" in [d.name for d in skill.dependencies]
        code = skill.generate()
        assert "tests/conftest.py" in code

class TestAgentIntegration:
    """Tests for Architecture and Production agent integration."""

    def test_agent_factory_instantiation(self):
        """Test that all required agents can be instantiated via factory."""
        agent_names = [
            "system_design", "tech_stack", "security_planning",
            "frontend", "backend", "testing", "devops"
        ]
        for name in agent_names:
            agent = AgentFactory.create_agent(name)
            assert agent is not None
            assert agent.name != ""

    @pytest.mark.asyncio
    async def test_architecture_agent_execution(self):
        """Test that an architecture agent can execute a task."""
        agent = AgentFactory.create_agent("system_design")
        task = AgentTask(name="Design SaaS", description="Design a scalable SaaS architecture")
        result = await agent.execute_task(task)
        # Architecture agent uses 'architecture' key, not 'architecture_specs'
        assert "architecture" in result
        assert "components" in result

    @pytest.mark.asyncio
    async def test_production_agent_execution(self):
        """Test that a production agent can execute a task."""
        agent = AgentFactory.create_agent("backend")
        task = AgentTask(name="Implement Auth", description="Implement JWT authentication")
        result = await agent.execute_task(task)
        assert "api_design" in result
        assert "database_schema" in result

class TestCollaborationSystem:
    """Tests for the agent collaboration and orchestration system."""

    def test_collaboration_protocol(self):
        protocol = CollaborationProtocol()
        context = protocol.create_context("proj_123", "ideation", "saas")
        assert context.project_id == "proj_123"
        
        # Test context sharing - uses specific fields mapped from agent names
        protocol.share_context("proj_123", "System Design Agent", {"pattern": "3-tier"})
        updated_context = protocol.get_context("proj_123")
        assert updated_context.architecture == {"pattern": "3-tier"}

    def test_workflow_orchestration(self):
        protocol = CollaborationProtocol()
        # Need to define the workflow in the protocol instance
        protocol.define_workflow("ideation_phase", STANDARD_WORKFLOWS["ideation_phase"])
        
        next_agent = protocol.get_next_agent("ideation_phase", "System Design Agent")
        assert next_agent == "Tech Stack Agent"
        
        next_agent = protocol.get_next_agent("ideation_phase", "Tech Stack Agent")
        assert next_agent == "Security Planning Agent"
