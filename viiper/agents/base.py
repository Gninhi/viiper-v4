"""
Base agent class for VIIPER multi-agent system.

All specialized agents inherit from this base class.
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime


class AgentRole(str, Enum):
    """Agent role categories (RAPS V2.0)."""
    
    RESEARCH = "research"          # Research agents
    ARCHITECTURE = "architecture"  # Architecture agents
    PRODUCTION = "production"      # Production agents
    SUPPORT = "support"            # Support agents
    SPECIALIST = "specialist"      # Specialist agents (spawned on-demand)
    
    @property
    def display_name(self) -> str:
        """Get display name."""
        return self.value.capitalize()


class AgentCapability(str, Enum):
    """Agent capabilities."""
    
    # Research capabilities
    MARKET_RESEARCH = "market_research"
    USER_INTERVIEWS = "user_interviews"
    COMPETITIVE_ANALYSIS = "competitive_analysis"
    DATA_ANALYSIS = "data_analysis"
    
    # Architecture capabilities
    SYSTEM_DESIGN = "system_design"
    TECH_STACK_SELECTION = "tech_stack_selection"
    SECURITY_PLANNING = "security_planning"
    SCALABILITY_PLANNING = "scalability_planning"
    
    # Production capabilities
    FRONTEND_DEVELOPMENT = "frontend_development"
    BACKEND_DEVELOPMENT = "backend_development"
    DATABASE_DESIGN = "database_design"
    TESTING = "testing"
    DEVOPS = "devops"
    
    # Support capabilities
    DOCUMENTATION = "documentation"
    MONITORING = "monitoring"
    CUSTOMER_SUPPORT = "customer_support"
    MAINTENANCE = "maintenance"
    
    # Specialist capabilities
    SEO = "seo"
    SECURITY_AUDIT = "security_audit"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    ACCESSIBILITY = "accessibility"
    PAYMENT_INTEGRATION = "payment_integration"


class AgentTask(BaseModel):
    """A task assigned to an agent."""
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: str
    priority: int = Field(ge=1, le=10, default=5)
    status: str = Field(default="pending")  # pending, in_progress, completed, failed
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class Agent(ABC, BaseModel):
    """
    Base class for all VIIPER agents.
    
    Agents are specialized, autonomous units that execute specific
    tasks within the VIIPER framework.
    """
    
    # Identity
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(description="Agent name")
    role: AgentRole = Field(description="Agent role category")
    
    # Capabilities
    capabilities: List[AgentCapability] = Field(
        default_factory=list,
        description="List of agent capabilities"
    )
    skills: List[str] = Field(
        default_factory=list,
        description="Specific skills this agent possesses"
    )
    
    # State
    status: str = Field(default="idle", description="Current status")
    current_task: Optional[AgentTask] = Field(default=None)
    completed_tasks: List[AgentTask] = Field(default_factory=list)
    
    # Performance
    success_rate: float = Field(default=1.0, ge=0.0, le=1.0)
    total_tasks: int = Field(default=0, ge=0)
    
    # Configuration
    max_parallel_tasks: int = Field(default=1, ge=1)
    auto_learn: bool = Field(default=True, description="Learn from experiences")
    
    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True
    
    @abstractmethod
    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute a task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result dictionary
        """
        pass
    
    def can_handle(self, capability: AgentCapability) -> bool:
        """Check if agent can handle a specific capability."""
        return capability in self.capabilities
    
    def assign_task(self, task: AgentTask) -> bool:
        """
        Assign a task to this agent.
        
        Returns:
            True if task assigned successfully, False otherwise
        """
        if self.current_task is not None:
            return False  # Already has a task
        
        self.current_task = task
        self.status = "busy"
        task.status = "in_progress"
        return True
    
    def complete_task(self, result: Dict[str, Any]) -> None:
        """Mark current task as completed."""
        if self.current_task:
            self.current_task.status = "completed"
            self.current_task.completed_at = datetime.now()
            self.current_task.result = result
            
            self.completed_tasks.append(self.current_task)
            self.total_tasks += 1
            self.current_task = None
            self.status = "idle"
            
            # Update success rate
            successful = len([t for t in self.completed_tasks if t.status == "completed"])
            self.success_rate = successful / self.total_tasks if self.total_tasks > 0 else 1.0
    
    def fail_task(self, error: str) -> None:
        """Mark current task as failed."""
        if self.current_task:
            self.current_task.status = "failed"
            self.current_task.completed_at = datetime.now()
            self.current_task.error = error
            
            self.completed_tasks.append(self.current_task)
            self.total_tasks += 1
            self.current_task = None
            self.status = "idle"
            
            # Update success rate
            successful = len([t for t in self.completed_tasks if t.status == "completed"])
            self.success_rate = successful / self.total_tasks if self.total_tasks > 0 else 1.0
    
    async def collaborate(self, other_agent: "Agent", message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collaborate with another agent.
        
        Args:
            other_agent: Agent to collaborate with
            message: Message/data to share
            
        Returns:
            Response from other agent
        """
        # Base implementation - can be overridden
        return {
            "from": self.name,
            "to": other_agent.name,
            "message": "Collaboration acknowledged",
            "data": message
        }
    
    def learn(self, experience: Dict[str, Any]) -> None:
        """
        Learn from an experience.
        
        This updates the agent's knowledge base (future: CKB integration).
        """
        if not self.auto_learn:
            return
        
        # Base implementation - can be extended
        # In production, this would update the Collective Knowledge Base
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics."""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role.display_name,
            "status": self.status,
            "capabilities": [cap.value for cap in self.capabilities],
            "skills": self.skills,
            "performance": {
                "total_tasks": self.total_tasks,
                "completed": len([t for t in self.completed_tasks if t.status == "completed"]),
                "failed": len([t for t in self.completed_tasks if t.status == "failed"]),
                "success_rate": f"{self.success_rate * 100:.1f}%"
            },
            "current_task": self.current_task.name if self.current_task else None
        }
    
    def __str__(self) -> str:
        """String representation."""
        stats = self.get_stats()
        return (
            f"\n{self.name} ({self.role.display_name} Agent)\n"
            f"Status: {self.status}\n"
            f"Capabilities: {', '.join([c.value for c in self.capabilities])}\n"
            f"Performance: {stats['performance']['success_rate']} "
            f"({stats['performance']['completed']}/{stats['performance']['total_tasks']} tasks)\n"
        )
