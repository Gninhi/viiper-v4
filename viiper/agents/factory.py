"""
Agent factory for dynamic agent instantiation.

Provides centralized agent creation and management.
"""

from typing import Dict, Type, Optional, List
from viiper.agents.base import Agent, AgentRole, AgentCapability
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


class AgentRegistry:
    """
    Registry of available agents.

    Maintains catalog of agent types and their capabilities.
    """

    # Map agent names to their classes
    AGENT_CLASSES: Dict[str, Type[Agent]] = {
        # Research agents
        "market_research": MarketResearchAgent,
        "user_interview": UserInterviewAgent,
        # Architecture agents
        "system_design": SystemDesignAgent,
        "tech_stack": TechStackAgent,
        "security_planning": SecurityPlanningAgent,
        # Production agents
        "frontend": FrontendAgent,
        "backend": BackendAgent,
        "testing": TestingAgent,
        "devops": DevOpsAgent,
    }

    # Map roles to agent names
    AGENTS_BY_ROLE: Dict[AgentRole, List[str]] = {
        AgentRole.RESEARCH: ["market_research", "user_interview"],
        AgentRole.ARCHITECTURE: ["system_design", "tech_stack", "security_planning"],
        AgentRole.PRODUCTION: ["frontend", "backend", "testing", "devops"],
        AgentRole.SUPPORT: [],  # To be added
        AgentRole.SPECIALIST: [],  # To be added
    }

    # Map capabilities to agent names
    AGENTS_BY_CAPABILITY: Dict[AgentCapability, List[str]] = {
        AgentCapability.MARKET_RESEARCH: ["market_research"],
        AgentCapability.USER_INTERVIEWS: ["user_interview"],
        AgentCapability.COMPETITIVE_ANALYSIS: ["market_research"],
        AgentCapability.DATA_ANALYSIS: ["market_research", "user_interview"],
        AgentCapability.SYSTEM_DESIGN: ["system_design"],
        AgentCapability.TECH_STACK_SELECTION: ["tech_stack"],
        AgentCapability.SECURITY_PLANNING: ["security_planning"],
        AgentCapability.SCALABILITY_PLANNING: ["system_design"],
        AgentCapability.FRONTEND_DEVELOPMENT: ["frontend"],
        AgentCapability.BACKEND_DEVELOPMENT: ["backend"],
        AgentCapability.DATABASE_DESIGN: ["backend"],
        AgentCapability.TESTING: ["testing"],
        AgentCapability.DEVOPS: ["devops"],
    }

    @classmethod
    def get_agent_class(cls, agent_name: str) -> Optional[Type[Agent]]:
        """
        Get agent class by name.

        Args:
            agent_name: Agent identifier (e.g., "market_research")

        Returns:
            Agent class or None if not found
        """
        return cls.AGENT_CLASSES.get(agent_name)

    @classmethod
    def get_agents_by_role(cls, role: AgentRole) -> List[str]:
        """
        Get all agent names for a role.

        Args:
            role: Agent role

        Returns:
            List of agent names
        """
        return cls.AGENTS_BY_ROLE.get(role, [])

    @classmethod
    def get_agents_by_capability(cls, capability: AgentCapability) -> List[str]:
        """
        Get all agent names with a capability.

        Args:
            capability: Agent capability

        Returns:
            List of agent names
        """
        return cls.AGENTS_BY_CAPABILITY.get(capability, [])

    @classmethod
    def list_all_agents(cls) -> List[str]:
        """
        List all available agent names.

        Returns:
            List of agent identifiers
        """
        return list(cls.AGENT_CLASSES.keys())


class AgentFactory:
    """
    Factory for creating agent instances.

    Provides centralized agent instantiation with proper initialization.
    """

    @staticmethod
    def create_agent(agent_name: str) -> Optional[Agent]:
        """
        Create agent instance by name.

        Args:
            agent_name: Agent identifier (e.g., "market_research")

        Returns:
            Instantiated agent or None if not found

        Example:
            >>> agent = AgentFactory.create_agent("system_design")
            >>> isinstance(agent, SystemDesignAgent)
            True
        """
        agent_class = AgentRegistry.get_agent_class(agent_name)
        if agent_class is None:
            return None

        # Instantiate agent
        return agent_class()

    @staticmethod
    def create_agents_for_role(role: AgentRole) -> List[Agent]:
        """
        Create all agents for a specific role.

        Args:
            role: Agent role

        Returns:
            List of instantiated agents

        Example:
            >>> agents = AgentFactory.create_agents_for_role(AgentRole.RESEARCH)
            >>> len(agents)
            2
        """
        agent_names = AgentRegistry.get_agents_by_role(role)
        agents = []

        for name in agent_names:
            agent = AgentFactory.create_agent(name)
            if agent:
                agents.append(agent)

        return agents

    @staticmethod
    def create_agents_for_phase(phase: str) -> List[Agent]:
        """
        Create appropriate agents for a VIIPER phase.

        Args:
            phase: VIIPER phase (validation, ideation, production, etc.)

        Returns:
            List of agents suitable for the phase

        Example:
            >>> agents = AgentFactory.create_agents_for_phase("ideation")
            >>> len(agents)
            3  # SystemDesign, TechStack, SecurityPlanning
        """
        # Map phases to required agents
        phase_agents = {
            "validation": ["market_research", "user_interview"],
            "ideation": ["system_design", "tech_stack", "security_planning"],
            "production": ["frontend", "backend", "testing", "devops"],
            "execution": [],  # Marketing/launch agents (future)
            "rentabilisation": [],  # Analytics/optimization agents (future)
            "iteration": ["frontend", "backend", "testing"],  # Subset for iteration
        }

        agent_names = phase_agents.get(phase.lower(), [])
        agents = []

        for name in agent_names:
            agent = AgentFactory.create_agent(name)
            if agent:
                agents.append(agent)

        return agents

    @staticmethod
    def create_agent_pool(size: int = None) -> List[Agent]:
        """
        Create a pool of all available agents.

        Args:
            size: Maximum pool size (None for all agents)

        Returns:
            List of all instantiated agents

        Example:
            >>> pool = AgentFactory.create_agent_pool()
            >>> len(pool)
            9  # All available agents
        """
        agent_names = AgentRegistry.list_all_agents()

        if size is not None:
            agent_names = agent_names[:size]

        agents = []
        for name in agent_names:
            agent = AgentFactory.create_agent(name)
            if agent:
                agents.append(agent)

        return agents

    @staticmethod
    def get_agent_info(agent_name: str) -> Optional[Dict]:
        """
        Get information about an agent without instantiating it.

        Args:
            agent_name: Agent identifier

        Returns:
            Agent metadata or None if not found

        Example:
            >>> info = AgentFactory.get_agent_info("system_design")
            >>> info['role']
            'architecture'
        """
        agent_class = AgentRegistry.get_agent_class(agent_name)
        if agent_class is None:
            return None

        # Get default values from class
        agent = agent_class()

        return {
            "name": agent.name,
            "role": agent.role.value,
            "capabilities": [cap.value for cap in agent.capabilities],
            "skills": agent.skills,
        }


# Convenience functions for common use cases


def create_ideation_team() -> List[Agent]:
    """
    Create team of agents for Ideation phase.

    Returns:
        List of architecture agents
    """
    return AgentFactory.create_agents_for_phase("ideation")


def create_production_team() -> List[Agent]:
    """
    Create team of agents for Production phase.

    Returns:
        List of production agents
    """
    return AgentFactory.create_agents_for_phase("production")


def create_validation_team() -> List[Agent]:
    """
    Create team of agents for Validation phase.

    Returns:
        List of research agents
    """
    return AgentFactory.create_agents_for_phase("validation")


def create_full_team() -> List[Agent]:
    """
    Create full team of all available agents.

    Returns:
        List of all agents
    """
    return AgentFactory.create_agent_pool()
