"""Agent system initialization."""

from viiper.agents.base import Agent, AgentCapability, AgentRole, AgentTask
from viiper.agents.research import MarketResearchAgent, UserInterviewAgent
from viiper.agents.architecture import (
    SystemDesignAgent,
    TechStackAgent,
    SecurityPlanningAgent,
)
from viiper.agents.production import (
    FrontendAgent,
    BackendAgent,
    TestingAgent,
    DevOpsAgent,
)
from viiper.agents.elite_frontend import EliteFrontendAgent
from viiper.agents.elite_architecture import EliteSystemDesignAgent
from viiper.agents.support import DocumentationAgent
from viiper.agents.specialist import SEOAgent, ContentWriterAgent
from viiper.agents.design_excellence import (
    DesignExcellenceGuide,
    DesignPhilosophy,
    ColorSystem,
    TypographySystem,
    AnimationSystem,
    ComponentLibrary,
)
from viiper.agents.collaboration import (
    AgentMessage,
    MessageType,
    SharedContext,
    CollaborationProtocol,
    STANDARD_WORKFLOWS,
)
from viiper.agents.factory import (
    AgentFactory,
    AgentRegistry,
    create_ideation_team,
    create_production_team,
    create_validation_team,
    create_full_team,
    create_elite_team,
)

# New agents for Browse → Idea → Code pipeline
from viiper.agents.browser import BrowserAgent, BrowserCapability
from viiper.agents.idea_generation import IdeaGenerationAgent, AppIdea, IdeaScore, IdeaCategory

# Phase E: Execution agents
from viiper.agents.execution import MarketingAgent, GrowthAgent, LaunchAgent

# Phase R: Rentabilisation agents
from viiper.agents.rentabilisation import MonetizationAgent, AnalyticsAgent, OptimizationAgent

__all__ = [
    # Base classes
    "Agent",
    "AgentCapability",
    "AgentRole",
    "AgentTask",
    # Research agents
    "MarketResearchAgent",
    "UserInterviewAgent",
    # Architecture agents
    "SystemDesignAgent",
    "TechStackAgent",
    "SecurityPlanningAgent",
    # Production agents
    "FrontendAgent",
    "BackendAgent",
    "TestingAgent",
    "DevOpsAgent",
    # Elite agents
    "EliteFrontendAgent",
    "EliteSystemDesignAgent",
    # Support agents
    "DocumentationAgent",
    # Specialist agents
    "SEOAgent",
    "ContentWriterAgent",
    # NEW: Browser & Idea agents
    "BrowserAgent",
    "BrowserCapability",
    "IdeaGenerationAgent",
    "AppIdea",
    "IdeaScore",
    "IdeaCategory",
    # Design Excellence
    "DesignExcellenceGuide",
    "DesignPhilosophy",
    "ColorSystem",
    "TypographySystem",
    "AnimationSystem",
    "ComponentLibrary",
    # Collaboration
    "AgentMessage",
    "MessageType",
    "SharedContext",
    "CollaborationProtocol",
    "STANDARD_WORKFLOWS",
    # Factory
    "AgentFactory",
    "AgentRegistry",
    "create_ideation_team",
    "create_production_team",
    "create_validation_team",
    "create_full_team",
    "create_elite_team",
    # Phase E: Execution
    "MarketingAgent",
    "GrowthAgent",
    "LaunchAgent",
    # Phase R: Rentabilisation
    "MonetizationAgent",
    "AnalyticsAgent",
    "OptimizationAgent",
]
