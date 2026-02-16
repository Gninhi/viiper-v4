"""
Project Orchestrator for VIIPER framework.

Coordinates agents, manages workflows, and ensures project execution.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import asyncio

from viiper.core.project import Project
from viiper.core.phase import Phase
from viiper.agents.base import Agent, AgentTask, AgentRole, AgentCapability
from viiper.agents.factory import AgentFactory
from viiper.agents.collaboration import CollaborationProtocol, MessageType


class OrchestrationResult(BaseModel):
    """Result of orchestrated execution."""
    
    success: bool
    phase: Phase
    tasks_completed: int = 0
    tasks_failed: int = 0
    results: List[Dict[str, Any]] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    duration_seconds: float = 0.0


class ProjectOrchestrator:
    """
    Main orchestrator for VIIPER projects.
    
    Responsibilities:
    - Agent coordination
    - Task distribution
    - Workflow management
    - Phase transitions
    """
    
    def __init__(self, project: Project, auto_register_agents: bool = True):
        """
        Initialize orchestrator.

        Args:
            project: Project to orchestrate
            auto_register_agents: Automatically register all available agents
        """
        self.project = project
        self.agents: List[Agent] = []
        self.active_tasks: List[AgentTask] = []
        self.collaboration = CollaborationProtocol()

        # Create shared context for this project
        self.context = self.collaboration.create_context(
            project_id=project.id,
            phase=project.phase.value,
            variant=project.variant.value
        )

        # Auto-register agents if requested
        if auto_register_agents:
            self._register_all_agents()
    
    def _register_all_agents(self) -> None:
        """Register all available agents using the factory."""
        all_agents = AgentFactory.create_agent_pool()
        for agent in all_agents:
            self.register_agent(agent)

    def register_agent(self, agent: Agent) -> None:
        """Register an agent with the orchestrator."""
        self.agents.append(agent)
    
    def get_agents_by_role(self, role: AgentRole) -> List[Agent]:
        """Get all agents with specific role."""
        return [agent for agent in self.agents if agent.role == role]
    
    def find_capable_agent(self, task: AgentTask) -> Optional[Agent]:
        """
        Find an agent capable of handling a task.

        Args:
            task: Task to assign

        Returns:
            Agent if found, None otherwise
        """
        # Map task names to required capabilities
        capability_map = {
            "Market Research": AgentCapability.MARKET_RESEARCH,
            "User Interviews": AgentCapability.USER_INTERVIEWS,
            "Competitive Analysis": AgentCapability.COMPETITIVE_ANALYSIS,
            "System Architecture": AgentCapability.SYSTEM_DESIGN,
            "Tech Stack Selection": AgentCapability.TECH_STACK_SELECTION,
            "Security Planning": AgentCapability.SECURITY_PLANNING,
            "Frontend Development": AgentCapability.FRONTEND_DEVELOPMENT,
            "Backend Development": AgentCapability.BACKEND_DEVELOPMENT,
            "Testing": AgentCapability.TESTING,
            "DevOps": AgentCapability.DEVOPS,
        }

        required_capability = capability_map.get(task.name)

        # Find agents with the required capability
        capable_agents = []
        for agent in self.agents:
            if required_capability and required_capability in agent.capabilities:
                capable_agents.append(agent)

        # Prefer idle agents, but allow busy agents if necessary
        idle_agents = [a for a in capable_agents if a.status == "idle"]
        if idle_agents:
            return idle_agents[0]
        elif capable_agents:
            return capable_agents[0]

        return None
    
    async def execute_phase(self, phase: Optional[Phase] = None) -> OrchestrationResult:
        """
        Execute tasks for a specific phase with agent collaboration.

        Args:
            phase: Phase to execute (defaults to current project phase)

        Returns:
            Orchestration result
        """
        import time
        start_time = time.time()

        target_phase = phase or self.project.phase

        # Update context phase
        self.context.phase = target_phase.value

        # Get tasks for this phase
        tasks = self._generate_phase_tasks(target_phase)

        # Execute tasks with collaboration
        results = []
        errors = []

        for task in tasks:
            try:
                agent = self.find_capable_agent(task)
                if not agent:
                    errors.append(f"No agent available for task: {task.name}")
                    continue

                # Get relevant context for this agent
                relevant_context = self.context.get_relevant_context(agent.name)

                # Add context to task if available
                if relevant_context:
                    task.context = relevant_context

                # Assign and execute
                agent.assign_task(task)
                result = await agent.execute_task(task)
                agent.complete_task(result)
                results.append(result)

                # Share agent output with context
                self.collaboration.share_context(
                    self.project.id,
                    agent.name,
                    result
                )

            except Exception as e:
                errors.append(f"Task {task.name} failed: {str(e)}")
                if agent:
                    agent.fail_task(str(e))

        duration = time.time() - start_time

        return OrchestrationResult(
            success=len(errors) == 0,
            phase=target_phase,
            tasks_completed=len(results),
            tasks_failed=len(errors),
            results=results,
            errors=errors,
            duration_seconds=duration
        )
    
    def _generate_phase_tasks(self, phase: Phase) -> List[AgentTask]:
        """
        Generate tasks for a specific phase.
        
        This is a simplified version. In production, tasks would be
        generated based on project requirements and CKB patterns.
        """
        tasks = []
        
        if phase == Phase.VALIDATION:
            tasks.extend([
                AgentTask(
                    name="Market Research",
                    description="Analyze market size and competition",
                    priority=10
                ),
                AgentTask(
                    name="User Interviews",
                    description="Conduct 10+ user interviews",
                    priority=9
                ),
                AgentTask(
                    name="Competitive Analysis",
                    description="Analyze top 5 competitors",
                    priority=8
                )
            ])
        
        elif phase == Phase.IDEATION:
            tasks.extend([
                AgentTask(
                    name="System Architecture",
                    description="Design system architecture",
                    priority=10
                ),
                AgentTask(
                    name="Tech Stack Selection",
                    description="Select optimal tech stack",
                    priority=9
                ),
                AgentTask(
                    name="Security Planning",
                    description="Plan security measures",
                    priority=8
                )
            ])
        
        elif phase == Phase.PRODUCTION:
            tasks.extend([
                AgentTask(
                    name="Frontend Development",
                    description="Build frontend application",
                    priority=10
                ),
                AgentTask(
                    name="Backend Development",
                    description="Build backend services",
                    priority=10
                ),
                AgentTask(
                    name="Testing",
                    description="Write and execute tests",
                    priority=9
                )
            ])
        
        # Add more phase-specific tasks...
        
        return tasks
    
    async def transition_phase(self, next_phase: Phase) -> bool:
        """
        Transition project to next phase with validation.
        
        Args:
            next_phase: Phase to transition to
            
        Returns:
            True if transition successful
        """
        # Check if transition is valid
        if not self.project._can_transition_to(next_phase):
            return False
        
        # Execute quality gates (simplified for Phase 0)
        # In production, this would run comprehensive validation
        
        # Transition
        success = self.project.transition_to_phase(next_phase)
        
        return success
    
    def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status."""
        return {
            "project": self.project.name,
            "current_phase": self.project.phase.display_name,
            "agents_registered": len(self.agents),
            "agents_active": len([a for a in self.agents if a.status == "busy"]),
            "agents_idle": len([a for a in self.agents if a.status == "idle"]),
            "active_tasks": len(self.active_tasks),
            "project_health": self.project.calculate_health_score().overall
        }
