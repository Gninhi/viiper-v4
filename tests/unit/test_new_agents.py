"""
Tests for new Browse → Idea → Code agents.

Tests BrowserAgent and IdeaGenerationAgent functionality.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


# Test BrowserAgent without actual browser
class TestBrowserAgent:
    """Tests for BrowserAgent class."""

    def test_browser_agent_creation(self):
        """Test that BrowserAgent can be instantiated."""
        from viiper.agents.browser import BrowserAgent, BrowserCapability
        
        agent = BrowserAgent()
        
        assert agent.name == "Browser Agent"
        assert agent.role.value == "specialist"
        assert BrowserCapability.WEB_NAVIGATION in agent.capabilities
        assert BrowserCapability.SEARCH in agent.capabilities

    def test_browser_agent_capabilities(self):
        """Test BrowserAgent capabilities."""
        from viiper.agents.browser import BrowserAgent, BrowserCapability
        
        agent = BrowserAgent()
        
        expected_capabilities = [
            BrowserCapability.WEB_NAVIGATION,
            BrowserCapability.CONTENT_SCRAPING,
            BrowserCapability.SCREENSHOT_CAPTURE,
            BrowserCapability.FORM_INTERACTION,
            BrowserCapability.SEARCH,
        ]
        
        for cap in expected_capabilities:
            assert cap in agent.capabilities, f"Missing capability: {cap}"

    def test_browser_agent_skills(self):
        """Test BrowserAgent skills list."""
        from viiper.agents.browser import BrowserAgent
        
        agent = BrowserAgent()
        
        assert "playwright" in agent.skills
        assert "web_scraping" in agent.skills
        assert "search_queries" in agent.skills


class TestIdeaGenerationAgent:
    """Tests for IdeaGenerationAgent class."""

    def test_idea_agent_creation(self):
        """Test that IdeaGenerationAgent can be instantiated."""
        from viiper.agents.idea_generation import IdeaGenerationAgent
        
        agent = IdeaGenerationAgent()
        
        assert agent.name == "Idea Generation Agent"
        assert agent.role.value == "research"

    def test_idea_agent_capabilities(self):
        """Test IdeaGenerationAgent capabilities."""
        from viiper.agents.idea_generation import IdeaGenerationAgent
        from viiper.agents.base import AgentCapability
        
        agent = IdeaGenerationAgent()
        
        assert AgentCapability.MARKET_RESEARCH in agent.capabilities
        assert AgentCapability.COMPETITIVE_ANALYSIS in agent.capabilities

    def test_keyword_extraction(self):
        """Test keyword extraction from text."""
        from viiper.agents.idea_generation import IdeaGenerationAgent
        
        agent = IdeaGenerationAgent()
        
        text = "Looking for AI automation tools for productivity and workflow management"
        keywords = agent._extract_keywords(text)
        
        assert "AI" in keywords
        assert "automation" in keywords
        assert "productivity" in keywords
        assert "workflow" in keywords

    def test_pain_points_identification(self):
        """Test pain point identification."""
        from viiper.agents.idea_generation import IdeaGenerationAgent
        
        agent = IdeaGenerationAgent()
        
        text = "I wish there was an easier way to manage tasks. Why is it so hard to find good tools?"
        pain_points = agent._identify_pain_points(text)
        
        assert len(pain_points) > 0
        assert any("wish there was" in p.lower() for p in pain_points)

    def test_market_gaps_identification(self):
        """Test market gap identification."""
        from viiper.agents.idea_generation import IdeaGenerationAgent
        
        agent = IdeaGenerationAgent()
        
        gaps = agent._find_market_gaps([])
        
        assert len(gaps) > 0
        assert any("AI" in gap for gap in gaps)

    def test_market_size_estimation(self):
        """Test market size estimation."""
        from viiper.agents.idea_generation import IdeaGenerationAgent, AppIdea, IdeaCategory, IdeaScore
        
        agent = IdeaGenerationAgent()
        
        # Test different categories
        saas_idea = AppIdea(
            id="test",
            title="Test SaaS",
            description="Test",
            category=IdeaCategory.SAAS
        )
        assert agent._estimate_market_size(saas_idea) == 0.8
        
        ai_idea = AppIdea(
            id="test",
            title="Test AI",
            description="Test",
            category=IdeaCategory.AI_PRODUCT
        )
        assert agent._estimate_market_size(ai_idea) == 0.9


class TestAppIdea:
    """Tests for AppIdea model."""

    def test_app_idea_creation(self):
        """Test AppIdea model creation."""
        from viiper.agents.idea_generation import AppIdea, IdeaCategory, IdeaScore
        
        idea = AppIdea(
            id="test_1",
            title="Test App",
            description="A test application",
            category=IdeaCategory.SAAS,
            key_features=["Feature 1", "Feature 2"],
            monetization=["Subscription"]
        )
        
        assert idea.title == "Test App"
        assert idea.category == IdeaCategory.SAAS
        assert len(idea.key_features) == 2

    def test_idea_score(self):
        """Test IdeaScore model."""
        from viiper.agents.idea_generation import IdeaScore
        
        score = IdeaScore(
            market_size=0.8,
            competition=0.3,
            feasibility=0.7,
            time_to_mvp=0.6,
            revenue_potential=0.75,
            overall=0.7
        )
        
        assert score.market_size == 0.8
        assert score.competition == 0.3
        assert score.overall == 0.7


class TestAgentFactory:
    """Tests for AgentFactory with new agents."""

    def test_create_browser_agent(self):
        """Test creating BrowserAgent via factory."""
        from viiper.agents.factory import AgentFactory
        from viiper.agents.browser import BrowserAgent
        
        agent = AgentFactory.create_agent("browser")
        
        assert agent is not None
        assert isinstance(agent, BrowserAgent)

    def test_create_idea_generation_agent(self):
        """Test creating IdeaGenerationAgent via factory."""
        from viiper.agents.factory import AgentFactory
        from viiper.agents.idea_generation import IdeaGenerationAgent
        
        agent = AgentFactory.create_agent("idea_generation")
        
        assert agent is not None
        assert isinstance(agent, IdeaGenerationAgent)

    def test_create_discovery_team(self):
        """Test creating discovery team."""
        from viiper.agents.factory import create_discovery_team
        
        team = create_discovery_team()
        
        assert len(team) == 2  # browser + idea_generation

    def test_create_browse_idea_code_pipeline(self):
        """Test creating full pipeline."""
        from viiper.agents.factory import create_browse_idea_code_pipeline
        
        pipeline = create_browse_idea_code_pipeline()
        
        assert "discovery" in pipeline
        assert "ideation" in pipeline
        assert "production" in pipeline
        
        assert len(pipeline["discovery"]) == 2
        assert len(pipeline["ideation"]) == 3
        assert len(pipeline["production"]) == 4


class TestAgentRegistry:
    """Tests for AgentRegistry with new agents."""

    def test_list_all_agents_includes_new(self):
        from viiper.agents.factory import AgentRegistry
        
        agents = AgentRegistry.list_all_agents()
        
        assert "browser" in agents
        assert "idea_generation" in agents

    def test_get_agents_by_role_includes_new(self):
        from viiper.agents.factory import AgentRegistry
        from viiper.agents.base import AgentRole
        
        research_agents = AgentRegistry.get_agents_by_role(AgentRole.RESEARCH)
        specialist_agents = AgentRegistry.get_agents_by_role(AgentRole.SPECIALIST)
        
        assert "idea_generation" in research_agents
        assert "browser" in specialist_agents


# Run with: pytest tests/unit/test_new_agents.py -v