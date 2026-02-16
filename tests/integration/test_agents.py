"""
Integration tests for VIIPER agents system.

Tests agent creation, collaboration, and orchestration.
"""

import pytest
import asyncio
from typing import List

from viiper.agents import (
    # Base
    Agent,
    AgentRole,
    AgentCapability,
    AgentTask,
    # Research agents
    MarketResearchAgent,
    UserInterviewAgent,
    # Architecture agents
    SystemDesignAgent,
    TechStackAgent,
    SecurityPlanningAgent,
    # Production agents
    FrontendAgent,
    BackendAgent,
    TestingAgent,
    DevOpsAgent,
    # Collaboration
    CollaborationProtocol,
    MessageType,
    SharedContext,
    STANDARD_WORKFLOWS,
    # Factory
    AgentFactory,
    AgentRegistry,
    create_ideation_team,
    create_production_team,
    create_validation_team,
    create_full_team,
)
from viiper.core.project import Project
from viiper.core.variant import Variant
from viiper.core.phase import Phase


# ============================================================================
# Test Agent Registry
# ============================================================================


class TestAgentRegistry:
    """Test agent registry functionality."""

    def test_list_all_agents(self):
        """Test listing all available agents."""
        agents = AgentRegistry.list_all_agents()
        assert len(agents) == 9
        assert "market_research" in agents
        assert "system_design" in agents
        assert "frontend" in agents

    def test_get_agent_class(self):
        """Test getting agent class by name."""
        agent_class = AgentRegistry.get_agent_class("system_design")
        assert agent_class == SystemDesignAgent

        agent_class = AgentRegistry.get_agent_class("frontend")
        assert agent_class == FrontendAgent

        agent_class = AgentRegistry.get_agent_class("nonexistent")
        assert agent_class is None

    def test_get_agents_by_role(self):
        """Test getting agents by role."""
        research_agents = AgentRegistry.get_agents_by_role(AgentRole.RESEARCH)
        assert len(research_agents) == 2
        assert "market_research" in research_agents
        assert "user_interview" in research_agents

        architecture_agents = AgentRegistry.get_agents_by_role(AgentRole.ARCHITECTURE)
        assert len(architecture_agents) == 3
        assert "system_design" in architecture_agents

        production_agents = AgentRegistry.get_agents_by_role(AgentRole.PRODUCTION)
        assert len(production_agents) == 4

    def test_get_agents_by_capability(self):
        """Test getting agents by capability."""
        design_agents = AgentRegistry.get_agents_by_capability(
            AgentCapability.SYSTEM_DESIGN
        )
        assert len(design_agents) == 1
        assert "system_design" in design_agents

        frontend_agents = AgentRegistry.get_agents_by_capability(
            AgentCapability.FRONTEND_DEVELOPMENT
        )
        assert len(frontend_agents) == 1
        assert "frontend" in frontend_agents


# ============================================================================
# Test Agent Factory
# ============================================================================


class TestAgentFactory:
    """Test agent factory functionality."""

    def test_create_agent(self):
        """Test creating single agent."""
        agent = AgentFactory.create_agent("system_design")
        assert agent is not None
        assert isinstance(agent, SystemDesignAgent)
        assert agent.name == "System Design Agent"
        assert agent.role == AgentRole.ARCHITECTURE

    def test_create_agent_nonexistent(self):
        """Test creating nonexistent agent."""
        agent = AgentFactory.create_agent("nonexistent")
        assert agent is None

    def test_create_agents_for_role(self):
        """Test creating agents for specific role."""
        agents = AgentFactory.create_agents_for_role(AgentRole.RESEARCH)
        assert len(agents) == 2
        assert all(isinstance(a, Agent) for a in agents)
        assert all(a.role == AgentRole.RESEARCH for a in agents)

    def test_create_agents_for_phase(self):
        """Test creating agents for VIIPER phases."""
        # Validation phase
        validation_agents = AgentFactory.create_agents_for_phase("validation")
        assert len(validation_agents) == 2
        agent_names = [a.name for a in validation_agents]
        assert "Market Research Agent" in agent_names

        # Ideation phase
        ideation_agents = AgentFactory.create_agents_for_phase("ideation")
        assert len(ideation_agents) == 3
        agent_names = [a.name for a in ideation_agents]
        assert "System Design Agent" in agent_names
        assert "Tech Stack Agent" in agent_names

        # Production phase
        production_agents = AgentFactory.create_agents_for_phase("production")
        assert len(production_agents) == 4
        agent_names = [a.name for a in production_agents]
        assert "Frontend Agent" in agent_names
        assert "Backend Agent" in agent_names

    def test_create_agent_pool(self):
        """Test creating pool of all agents."""
        pool = AgentFactory.create_agent_pool()
        assert len(pool) == 9
        assert all(isinstance(a, Agent) for a in pool)

        # Test with size limit
        limited_pool = AgentFactory.create_agent_pool(size=5)
        assert len(limited_pool) == 5

    def test_get_agent_info(self):
        """Test getting agent info without instantiation."""
        info = AgentFactory.get_agent_info("system_design")
        assert info is not None
        assert info["name"] == "System Design Agent"
        assert info["role"] == "architecture"
        assert "system_design" in info["capabilities"]

        # Nonexistent agent
        info = AgentFactory.get_agent_info("nonexistent")
        assert info is None


# ============================================================================
# Test Convenience Functions
# ============================================================================


class TestConvenienceFunctions:
    """Test convenience team creation functions."""

    def test_create_validation_team(self):
        """Test creating validation team."""
        team = create_validation_team()
        assert len(team) == 2
        assert all(a.role == AgentRole.RESEARCH for a in team)

    def test_create_ideation_team(self):
        """Test creating ideation team."""
        team = create_ideation_team()
        assert len(team) == 3
        assert all(a.role == AgentRole.ARCHITECTURE for a in team)

    def test_create_production_team(self):
        """Test creating production team."""
        team = create_production_team()
        assert len(team) == 4
        assert all(a.role == AgentRole.PRODUCTION for a in team)

    def test_create_full_team(self):
        """Test creating full team."""
        team = create_full_team()
        assert len(team) == 9


# ============================================================================
# Test Individual Agents
# ============================================================================


class TestArchitectureAgents:
    """Test architecture agents."""

    @pytest.mark.asyncio
    async def test_system_design_agent(self):
        """Test SystemDesignAgent execution."""
        agent = SystemDesignAgent()
        assert agent.name == "System Design Agent"
        assert AgentCapability.SYSTEM_DESIGN in agent.capabilities

        task = AgentTask(
            name="Design System",
            description="Design a SaaS application architecture",
            priority=10,
        )

        result = await agent.execute_task(task)
        assert "architecture" in result
        assert "components" in result
        assert "scalability" in result
        assert result["confidence"] > 0

    @pytest.mark.asyncio
    async def test_tech_stack_agent(self):
        """Test TechStackAgent execution."""
        agent = TechStackAgent()
        assert agent.name == "Tech Stack Agent"
        assert AgentCapability.TECH_STACK_SELECTION in agent.capabilities

        task = AgentTask(
            name="Select Tech Stack",
            description="Select tech stack for SaaS variant",
            priority=9,
        )

        result = await agent.execute_task(task)
        assert "recommended_stack" in result
        assert "frontend" in result["recommended_stack"]
        assert "backend" in result["recommended_stack"]
        assert "alternatives" in result

    @pytest.mark.asyncio
    async def test_security_planning_agent(self):
        """Test SecurityPlanningAgent execution."""
        agent = SecurityPlanningAgent()
        assert agent.name == "Security Planning Agent"
        assert AgentCapability.SECURITY_PLANNING in agent.capabilities

        task = AgentTask(
            name="Plan Security",
            description="Create security plan for web application",
            priority=8,
        )

        result = await agent.execute_task(task)
        assert "security_checklist" in result
        assert "threat_model" in result
        assert "compliance" in result


class TestProductionAgents:
    """Test production agents."""

    @pytest.mark.asyncio
    async def test_frontend_agent(self):
        """Test FrontendAgent execution."""
        agent = FrontendAgent()
        assert agent.name == "Frontend Agent"
        assert AgentCapability.FRONTEND_DEVELOPMENT in agent.capabilities

        task = AgentTask(
            name="Design Frontend",
            description="Design frontend for SaaS application",
            priority=10,
        )

        result = await agent.execute_task(task)
        assert "component_structure" in result
        assert "state_management" in result
        assert "styling_strategy" in result

    @pytest.mark.asyncio
    async def test_backend_agent(self):
        """Test BackendAgent execution."""
        agent = BackendAgent()
        assert agent.name == "Backend Agent"
        assert AgentCapability.BACKEND_DEVELOPMENT in agent.capabilities

        task = AgentTask(
            name="Design Backend",
            description="Design backend API for SaaS",
            priority=10,
        )

        result = await agent.execute_task(task)
        assert "api_design" in result
        assert "database_schema" in result
        assert "architecture" in result

    @pytest.mark.asyncio
    async def test_testing_agent(self):
        """Test TestingAgent execution."""
        agent = TestingAgent()
        assert agent.name == "Testing Agent"
        assert AgentCapability.TESTING in agent.capabilities

        task = AgentTask(
            name="Create Test Strategy",
            description="Define testing strategy",
            priority=9,
        )

        result = await agent.execute_task(task)
        assert "strategy" in result
        assert "test_suites" in result
        assert "coverage_targets" in result

    @pytest.mark.asyncio
    async def test_devops_agent(self):
        """Test DevOpsAgent execution."""
        agent = DevOpsAgent()
        assert agent.name == "DevOps Agent"
        assert AgentCapability.DEVOPS in agent.capabilities

        task = AgentTask(
            name="Setup CI/CD",
            description="Setup deployment pipeline",
            priority=8,
        )

        result = await agent.execute_task(task)
        assert "ci_cd_pipeline" in result
        assert "deployment_strategy" in result
        assert "infrastructure" in result


# ============================================================================
# Test Collaboration System
# ============================================================================


class TestCollaboration:
    """Test agent collaboration."""

    def test_shared_context_creation(self):
        """Test creating shared context."""
        context = SharedContext(
            project_id="test-project",
            phase="ideation",
            variant="saas",
        )
        assert context.project_id == "test-project"
        assert context.phase == "ideation"
        assert context.architecture is None

    def test_shared_context_update(self):
        """Test updating shared context."""
        context = SharedContext(
            project_id="test-project",
            phase="ideation",
            variant="saas",
        )

        # Update from SystemDesignAgent
        context.update_from_agent(
            "System Design Agent",
            {"architecture": "Three-tier", "components": ["API", "DB"]},
        )
        assert context.architecture is not None
        assert context.architecture["architecture"] == "Three-tier"

        # Update from TechStackAgent
        context.update_from_agent(
            "Tech Stack Agent", {"frontend": "Next.js", "backend": "Node.js"}
        )
        assert context.tech_stack is not None

    def test_get_relevant_context(self):
        """Test getting relevant context for agents."""
        context = SharedContext(
            project_id="test-project",
            phase="production",
            variant="saas",
        )

        # Add architecture
        context.architecture = {"design": "microservices"}
        context.tech_stack = {"frontend": "Next.js"}
        context.api_design = {"endpoints": ["/api/users"]}

        # Frontend agent needs architecture, api_design, tech_stack
        frontend_context = context.get_relevant_context("Frontend Agent")
        assert "architecture" in frontend_context
        assert "api_design" in frontend_context
        assert "tech_stack" in frontend_context

        # Backend agent needs architecture, tech_stack, security_plan
        backend_context = context.get_relevant_context("Backend Agent")
        assert "architecture" in backend_context
        assert "tech_stack" in backend_context

    def test_collaboration_protocol(self):
        """Test collaboration protocol."""
        protocol = CollaborationProtocol()

        # Create context
        context = protocol.create_context("test-proj", "ideation", "saas")
        assert context is not None

        # Get context
        retrieved = protocol.get_context("test-proj")
        assert retrieved == context

    def test_message_passing(self):
        """Test agent message passing."""
        protocol = CollaborationProtocol()

        # Send message
        msg = protocol.send_message(
            from_agent="Frontend Agent",
            to_agent="Backend Agent",
            message_type=MessageType.REQUEST,
            subject="Need API endpoints",
            content={"query": "What endpoints are available?"},
            requires_response=True,
            priority=8,
        )

        assert msg.from_agent == "Frontend Agent"
        assert msg.to_agent == "Backend Agent"
        assert msg.requires_response is True

        # Get messages for agent
        messages = protocol.get_messages_for_agent("Backend Agent")
        assert len(messages) == 1
        assert messages[0].subject == "Need API endpoints"

    def test_workflow_definition(self):
        """Test workflow definition."""
        protocol = CollaborationProtocol()

        # Define workflow
        protocol.define_workflow(
            "ideation", ["System Design Agent", "Tech Stack Agent"]
        )

        # Get next agent
        next_agent = protocol.get_next_agent("ideation", "System Design Agent")
        assert next_agent == "Tech Stack Agent"

        # Last agent
        next_agent = protocol.get_next_agent("ideation", "Tech Stack Agent")
        assert next_agent is None

    def test_standard_workflows(self):
        """Test standard workflows are defined."""
        assert "ideation_phase" in STANDARD_WORKFLOWS
        assert "production_phase" in STANDARD_WORKFLOWS
        assert "full_stack_development" in STANDARD_WORKFLOWS

        ideation = STANDARD_WORKFLOWS["ideation_phase"]
        assert len(ideation) == 3
        assert "System Design Agent" in ideation


# ============================================================================
# Test End-to-End Workflows
# ============================================================================


class TestEndToEndWorkflows:
    """Test complete agent workflows."""

    @pytest.mark.asyncio
    async def test_ideation_workflow(self):
        """Test complete ideation phase workflow."""
        # Create agents
        team = create_ideation_team()
        assert len(team) == 3

        # Create shared context
        protocol = CollaborationProtocol()
        context = protocol.create_context("test-saas", "ideation", "saas")

        # Execute agents in sequence
        results = []
        for agent in team:
            task = AgentTask(
                name=f"{agent.name} Task",
                description=f"Execute {agent.name} for SaaS project",
                priority=10,
            )

            # Execute
            result = await agent.execute_task(task)
            results.append(result)

            # Share context
            protocol.share_context("test-saas", agent.name, result)

        # Verify all agents executed
        assert len(results) == 3
        assert all(r["confidence"] > 0 for r in results)

        # Verify context was shared
        final_context = protocol.get_context("test-saas")
        assert final_context.architecture is not None
        assert final_context.tech_stack is not None
        assert final_context.security_plan is not None

    @pytest.mark.asyncio
    async def test_production_workflow(self):
        """Test complete production phase workflow."""
        # Create agents
        team = create_production_team()
        assert len(team) == 4

        # Create shared context with architecture already done
        protocol = CollaborationProtocol()
        context = protocol.create_context("test-saas", "production", "saas")
        context.architecture = {"design": "three-tier"}
        context.tech_stack = {"frontend": "Next.js", "backend": "Node.js"}

        # Execute agents
        results = []
        for agent in team:
            task = AgentTask(
                name=f"{agent.name} Task",
                description=f"Execute {agent.name}",
                priority=10,
            )

            result = await agent.execute_task(task)
            results.append(result)

            protocol.share_context("test-saas", agent.name, result)

        # Verify execution
        assert len(results) == 4
        assert all(r["confidence"] > 0 for r in results)

    @pytest.mark.asyncio
    async def test_multi_phase_workflow(self):
        """Test workflow across multiple phases."""
        protocol = CollaborationProtocol()

        # Phase 1: Validation
        validation_team = create_validation_team()
        context = protocol.create_context("multi-phase", "validation", "saas")

        for agent in validation_team:
            task = AgentTask(
                name=f"{agent.name} Task", description="Validation task", priority=10
            )
            result = await agent.execute_task(task)
            protocol.share_context("multi-phase", agent.name, result)

        # Phase 2: Ideation
        ideation_team = create_ideation_team()
        context.phase = "ideation"

        for agent in ideation_team:
            task = AgentTask(
                name=f"{agent.name} Task", description="Ideation task", priority=10
            )

            result = await agent.execute_task(task)
            protocol.share_context("multi-phase", agent.name, result)

        # Verify context accumulated across phases
        final_context = protocol.get_context("multi-phase")
        assert final_context is not None
        assert final_context.architecture is not None
        assert final_context.tech_stack is not None


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])
