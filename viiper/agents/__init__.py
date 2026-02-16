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
]
