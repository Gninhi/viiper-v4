"""
Agent collaboration system for VIIPER framework.

Enables agents to communicate, share context, and coordinate tasks.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class MessageType(str, Enum):
    """Types of messages agents can exchange."""

    REQUEST = "request"  # Request information from another agent
    RESPONSE = "response"  # Respond to a request
    NOTIFICATION = "notification"  # Notify without expecting response
    CONTEXT_SHARE = "context_share"  # Share execution context
    TASK_DELEGATE = "task_delegate"  # Delegate a task to another agent


class AgentMessage(BaseModel):
    """
    Message passed between agents.

    Enables structured communication in multi-agent workflows.
    """

    id: str = Field(default_factory=lambda: f"msg_{datetime.now().timestamp()}")
    type: MessageType = Field(description="Message type")
    from_agent: str = Field(description="Sending agent ID")
    to_agent: str = Field(description="Receiving agent ID")
    subject: str = Field(description="Message subject/topic")
    content: Dict[str, Any] = Field(description="Message payload")
    timestamp: datetime = Field(default_factory=datetime.now)
    requires_response: bool = Field(default=False)
    priority: int = Field(default=5, ge=1, le=10, description="Priority 1-10")

    def __str__(self) -> str:
        return f"[{self.type}] {self.from_agent} → {self.to_agent}: {self.subject}"


class SharedContext(BaseModel):
    """
    Shared execution context between agents.

    Allows agents to build on each other's work without duplicating effort.
    """

    project_id: str = Field(description="Project this context belongs to")
    phase: str = Field(description="Current project phase")
    variant: str = Field(description="Project variant type")

    # Shared data from different agents
    architecture: Optional[Dict[str, Any]] = Field(
        default=None, description="System architecture from SystemDesignAgent"
    )
    tech_stack: Optional[Dict[str, Any]] = Field(
        default=None, description="Technology stack from TechStackAgent"
    )
    security_plan: Optional[Dict[str, Any]] = Field(
        default=None, description="Security planning from SecurityPlanningAgent"
    )
    api_design: Optional[Dict[str, Any]] = Field(
        default=None, description="API design from BackendAgent"
    )
    ui_structure: Optional[Dict[str, Any]] = Field(
        default=None, description="UI structure from FrontendAgent"
    )
    test_strategy: Optional[Dict[str, Any]] = Field(
        default=None, description="Test strategy from TestingAgent"
    )
    seo_strategy: Optional[Dict[str, Any]] = Field(
        default=None, description="SEO analysis and keyword strategy"
    )
    content: Optional[Dict[str, Any]] = Field(
        default=None, description="Generated content and copy"
    )
    documentation: Optional[Dict[str, Any]] = Field(
        default=None, description="Project documentation output"
    )
    deployment_plan: Optional[Dict[str, Any]] = Field(
        default=None, description="Deployment plan from DevOpsAgent"
    )

    # General metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def update_from_agent(self, agent_name: str, data: Dict[str, Any]) -> None:
        """
        Update context with agent's output.

        Args:
            agent_name: Name of the agent providing data
            data: Data from agent execution
        """
        # Map agent names to context fields
        agent_field_map = {
            "System Design Agent": "architecture",
            "Elite System Design Agent": "architecture",
            "Tech Stack Agent": "tech_stack",
            "Security Planning Agent": "security_plan",
            "Backend Agent": "api_design",
            "Frontend Agent": "ui_structure",
            "Elite Frontend Agent": "ui_structure",
            "Testing Agent": "test_strategy",
            "DevOps Agent": "deployment_plan",
            "SEO Agent": "seo_strategy",
            "Content Writer Agent": "content",
            "Documentation Agent": "documentation",
        }

        field = agent_field_map.get(agent_name)
        if field:
            setattr(self, field, data)
            self.updated_at = datetime.now()

    def get_relevant_context(self, requesting_agent: str) -> Dict[str, Any]:
        """
        Get context relevant to requesting agent.

        Args:
            requesting_agent: Agent requesting context

        Returns:
            Filtered context relevant to the agent
        """
        # Define what context each agent needs
        context_needs = {
            "Frontend Agent": ["architecture", "api_design", "tech_stack", "security_plan"],
            "Backend Agent": ["architecture", "tech_stack", "security_plan"],
            "Testing Agent": ["architecture", "api_design", "ui_structure", "tech_stack"],
            "DevOps Agent": ["architecture", "tech_stack", "api_design", "test_strategy"],
            "Tech Stack Agent": ["architecture"],
            "Security Planning Agent": ["architecture", "tech_stack"],
        }

        needed_fields = context_needs.get(requesting_agent, [])

        # Build relevant context
        relevant = {}
        for field in needed_fields:
            value = getattr(self, field, None)
            if value is not None:
                relevant[field] = value

        return relevant


class CollaborationProtocol:
    """
    Protocol for agent collaboration.

    Manages message passing, context sharing, and workflow coordination.
    """

    def __init__(self):
        """Initialize collaboration protocol."""
        self.contexts: Dict[str, SharedContext] = {}  # project_id -> context
        self.messages: List[AgentMessage] = []
        self.workflows: Dict[str, List[str]] = {}  # workflow_id -> [agent_names]

    def create_context(
        self, project_id: str, phase: str, variant: str
    ) -> SharedContext:
        """
        Create shared context for a project.

        Args:
            project_id: Project identifier
            phase: Current phase
            variant: Project variant

        Returns:
            Shared context
        """
        context = SharedContext(project_id=project_id, phase=phase, variant=variant)
        self.contexts[project_id] = context
        return context

    def get_context(self, project_id: str) -> Optional[SharedContext]:
        """
        Get shared context for a project.

        Args:
            project_id: Project identifier

        Returns:
            Shared context if exists
        """
        return self.contexts.get(project_id)

    def send_message(
        self,
        from_agent: str,
        to_agent: str,
        message_type: MessageType,
        subject: str,
        content: Dict[str, Any],
        requires_response: bool = False,
        priority: int = 5,
    ) -> AgentMessage:
        """
        Send message from one agent to another.

        Args:
            from_agent: Sending agent ID
            to_agent: Receiving agent ID
            message_type: Type of message
            subject: Message subject
            content: Message payload
            requires_response: Whether response is required
            priority: Message priority (1-10)

        Returns:
            Created message
        """
        message = AgentMessage(
            type=message_type,
            from_agent=from_agent,
            to_agent=to_agent,
            subject=subject,
            content=content,
            requires_response=requires_response,
            priority=priority,
        )

        self.messages.append(message)
        return message

    def get_messages_for_agent(
        self, agent_id: str, unread_only: bool = False
    ) -> List[AgentMessage]:
        """
        Get messages for a specific agent.

        Args:
            agent_id: Agent identifier
            unread_only: Only return unread messages

        Returns:
            List of messages
        """
        messages = [msg for msg in self.messages if msg.to_agent == agent_id]

        # Sort by priority (high to low) then timestamp
        messages.sort(key=lambda m: (-m.priority, m.timestamp))

        return messages

    def share_context(
        self, project_id: str, agent_name: str, agent_output: Dict[str, Any]
    ) -> None:
        """
        Share agent output with project context.

        Args:
            project_id: Project identifier
            agent_name: Name of agent sharing context
            agent_output: Output from agent execution
        """
        context = self.get_context(project_id)
        if context:
            context.update_from_agent(agent_name, agent_output)

    def define_workflow(
        self, workflow_id: str, agent_sequence: List[str]
    ) -> None:
        """
        Define a multi-agent workflow.

        Args:
            workflow_id: Workflow identifier
            agent_sequence: Ordered list of agent names
        """
        self.workflows[workflow_id] = agent_sequence

    def get_next_agent(self, workflow_id: str, current_agent: str) -> Optional[str]:
        """
        Get next agent in workflow sequence.

        Args:
            workflow_id: Workflow identifier
            current_agent: Current agent name

        Returns:
            Next agent name or None if end of workflow
        """
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return None

        try:
            current_index = workflow.index(current_agent)
            if current_index < len(workflow) - 1:
                return workflow[current_index + 1]
        except ValueError:
            pass

        return None


# Pre-defined workflows
STANDARD_WORKFLOWS = {
    "ideation_phase": [
        "System Design Agent",
        "Tech Stack Agent",
        "Security Planning Agent",
    ],
    "production_phase": [
        "Backend Agent",
        "Frontend Agent",
        "Testing Agent",
        "DevOps Agent",
    ],
    "full_stack_development": [
        "System Design Agent",
        "Tech Stack Agent",
        "Security Planning Agent",
        "Backend Agent",
        "Frontend Agent",
        "Testing Agent",
        "DevOps Agent",
    ],
}


def create_collaboration_example() -> Dict[str, Any]:
    """
    Create example of agent collaboration.

    Returns:
        Example workflow execution
    """
    # Initialize protocol
    protocol = CollaborationProtocol()

    # Create project context
    context = protocol.create_context(
        project_id="example-saas", phase="ideation", variant="saas"
    )

    # Define workflow
    protocol.define_workflow("ideation", STANDARD_WORKFLOWS["ideation_phase"])

    # Simulate agent execution and collaboration
    steps = []

    # Step 1: System Design Agent executes
    system_design_output = {
        "architecture": "Three-tier architecture",
        "components": ["Frontend", "API", "Database"],
        "scalability": "Horizontal scaling ready",
    }
    protocol.share_context("example-saas", "System Design Agent", system_design_output)
    steps.append("SystemDesignAgent completed, shared architecture")

    # Step 2: Tech Stack Agent requests architecture
    msg = protocol.send_message(
        from_agent="Tech Stack Agent",
        to_agent="System Design Agent",
        message_type=MessageType.REQUEST,
        subject="Need architecture details",
        content={"query": "What components need tech stack?"},
        requires_response=True,
    )
    steps.append(f"TechStackAgent requested info: {msg.id}")

    # Step 3: Tech Stack Agent executes with context
    relevant_context = context.get_relevant_context("Tech Stack Agent")
    steps.append(f"TechStackAgent received context: {list(relevant_context.keys())}")

    tech_stack_output = {
        "frontend": "Next.js",
        "backend": "Node.js",
        "database": "PostgreSQL",
    }
    protocol.share_context("example-saas", "Tech Stack Agent", tech_stack_output)
    steps.append("TechStackAgent completed, shared tech stack")

    # Step 4: Security Planning Agent uses both contexts
    relevant_context = context.get_relevant_context("Security Planning Agent")
    steps.append(
        f"SecurityPlanningAgent received context: {list(relevant_context.keys())}"
    )

    security_output = {
        "authentication": "JWT with NextAuth",
        "encryption": "TLS 1.3",
        "compliance": ["GDPR"],
    }
    protocol.share_context("example-saas", "Security Planning Agent", security_output)
    steps.append("SecurityPlanningAgent completed")

    return {
        "workflow": "ideation_phase",
        "context": context.model_dump(),
        "messages": [msg.model_dump() for msg in protocol.messages],
        "execution_steps": steps,
    }
