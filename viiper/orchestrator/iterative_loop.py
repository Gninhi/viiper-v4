"""
Iterative Agent Loop for autonomous task execution.

Implements the Analyze → Plan → Execute → Observe → Learn cycle
inspired by Manus AI architecture.
"""

from typing import Dict, Any, List, Optional, Callable
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
import asyncio
import traceback


class LoopState(str, Enum):
    """States of the iterative loop."""
    IDLE = "idle"
    ANALYZING = "analyzing"
    PLANNING = "planning"
    EXECUTING = "executing"
    OBSERVING = "observing"
    LEARNING = "learning"
    COMPLETED = "completed"
    FAILED = "failed"


class StepResult(BaseModel):
    """Result of a single step in the loop."""
    step_number: int
    action: str
    success: bool
    output: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class LoopMetrics(BaseModel):
    """Metrics for the iterative loop."""
    total_steps: int = 0
    successful_steps: int = 0
    failed_steps: int = 0
    total_duration_seconds: float = 0.0
    average_step_duration: float = 0.0
    learnings_count: int = 0


class IterativeAgentLoop:
    """
    Autonomous iterative execution loop.
    
    Implements the cycle:
    1. ANALYZE - Understand current state and requirements
    2. PLAN - Determine next actions
    3. EXECUTE - Perform the actions
    4. OBSSERVE - Monitor results
    5. LEARN - Update knowledge and adjust
    
    Step limits (inspired by Manus AI):
    - Orchestrator: 15 steps max
    - Sub-agents: 100 steps max
    
    Usage:
        loop = IterativeAgentLoop(
            agent=my_agent,
            task=task,
            max_steps=15
        )
        result = await loop.run()
    """
    
    # Step limits
    ORCHESTRATOR_MAX_STEPS = 15
    SUB_AGENT_MAX_STEPS = 100
    
    def __init__(
        self,
        agent,  # Agent instance
        task,  # AgentTask instance
        max_steps: int = None,
        on_step_complete: Optional[Callable] = None,
        on_learning: Optional[Callable] = None,
    ):
        """
        Initialize iterative loop.
        
        Args:
            agent: Agent to execute tasks
            task: Task to accomplish
            max_steps: Maximum steps (default: ORCHESTRATOR_MAX_STEPS)
            on_step_complete: Callback after each step
            on_learning: Callback when learning occurs
        """
        self.agent = agent
        self.task = task
        self.max_steps = max_steps or self.ORCHESTRATOR_MAX_STEPS
        
        # Callbacks
        self.on_step_complete = on_step_complete
        self.on_learning = on_learning
        
        # State
        self.state = LoopState.IDLE
        self.current_step = 0
        self.step_results: List[StepResult] = []
        self.learnings: List[Dict[str, Any]] = []
        self.context: Dict[str, Any] = {}
        self.metrics = LoopMetrics()
        
    async def run(self) -> Dict[str, Any]:
        """
        Execute the iterative loop until completion or failure.
        
        Returns:
            Final result with all step outputs
        """
        import time
        start_time = time.time()
        
        try:
            while self.current_step < self.max_steps:
                self.current_step += 1
                
                # Execute one iteration
                result = await self._execute_iteration()
                
                if result.get("completed", False):
                    self.state = LoopState.COMPLETED
                    break
                    
                if result.get("failed", False):
                    self.state = LoopState.FAILED
                    break
                    
            # Calculate final metrics
            self.metrics.total_steps = self.current_step
            self.metrics.total_duration_seconds = time.time() - start_time
            self.metrics.average_step_duration = (
                self.metrics.total_duration_seconds / max(self.current_step, 1)
            )
            
            return self._build_result()
            
        except Exception as e:
            self.state = LoopState.FAILED
            return {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc(),
                "metrics": self.metrics.model_dump(),
            }
    
    async def _execute_iteration(self) -> Dict[str, Any]:
        """Execute one full iteration of the loop."""
        step_start = datetime.now()
        
        # 1. ANALYZE
        self.state = LoopState.ANALYZING
        analysis = await self._analyze()
        
        # Check if we can complete
        if analysis.get("can_complete", False):
            return {"completed": True, "analysis": analysis}
        
        # 2. PLAN
        self.state = LoopState.PLANNING
        plan = await self._plan(analysis)
        
        if not plan.get("actions"):
            return {"completed": True, "reason": "No more actions to take"}
        
        # 3. EXECUTE
        self.state = LoopState.EXECUTING
        execution_result = await self._execute(plan)
        
        # 4. OBSERVE
        self.state = LoopState.OBSERVING
        observation = await self._observe(execution_result)
        
        # 5. LEARN
        self.state = LoopState.LEARNING
        learning = await self._learn(observation)
        
        # Record step result
        step_result = StepResult(
            step_number=self.current_step,
            action=plan.get("actions", ["unknown"])[0] if plan.get("actions") else "none",
            success=execution_result.get("success", False),
            output=observation,
            error=execution_result.get("error"),
        )
        self.step_results.append(step_result)
        
        # Update metrics
        if step_result.success:
            self.metrics.successful_steps += 1
        else:
            self.metrics.failed_steps += 1
        
        # Callback
        if self.on_step_complete:
            await self._safe_callback(self.on_step_complete, step_result.model_dump())
        
        # Check for failure
        if not execution_result.get("success") and execution_result.get("critical", False):
            return {"failed": True, "error": execution_result.get("error")}
        
        return {"completed": False, "step": step_result.model_dump()}
    
    async def _analyze(self) -> Dict[str, Any]:
        """
        Analyze current state and task requirements.
        
        Returns analysis with:
        - current_state: Where we are now
        - goal_state: Where we need to be
        - gaps: What's missing
        - can_complete: Whether we can complete now
        """
        analysis = {
            "current_state": self._get_current_state(),
            "goal_state": self._get_goal_state(),
            "gaps": [],
            "can_complete": False,
            "context": self.context,
        }
        
        # Determine gaps between current and goal state
        analysis["gaps"] = self._identify_gaps(
            analysis["current_state"],
            analysis["goal_state"]
        )
        
        # Check if we can complete
        analysis["can_complete"] = len(analysis["gaps"]) == 0
        
        # Update context
        self.context["last_analysis"] = analysis
        
        return analysis
    
    async def _plan(self, analysis: Dict) -> Dict[str, Any]:
        """
        Plan next actions based on analysis.
        
        Returns plan with:
        - actions: List of actions to take
        - priority: Action priority
        - estimated_impact: Expected outcome
        """
        gaps = analysis.get("gaps", [])
        
        if not gaps:
            return {"actions": [], "reason": "No gaps to address"}
        
        # Prioritize gaps and create actions
        actions = []
        for gap in gaps[:3]:  # Max 3 actions per iteration
            action = self._gap_to_action(gap)
            if action:
                actions.append(action)
        
        plan = {
            "actions": actions,
            "priority": self._calculate_priority(gaps),
            "estimated_impact": self._estimate_impact(actions),
        }
        
        self.context["last_plan"] = plan
        return plan
    
    async def _execute(self, plan: Dict) -> Dict[str, Any]:
        """
        Execute planned actions.
        
        Returns execution result with:
        - success: Whether execution succeeded
        - outputs: Action outputs
        - error: Error message if failed
        - critical: Whether failure is critical
        """
        actions = plan.get("actions", [])
        results = []
        
        for action in actions:
            try:
                # Execute action via agent
                result = await self._execute_action(action)
                results.append({
                    "action": action,
                    "success": result.get("success", True),
                    "output": result,
                })
                
                if not result.get("success", True):
                    return {
                        "success": False,
                        "error": result.get("error", "Action failed"),
                        "critical": action.get("critical", False),
                    }
                    
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "critical": action.get("critical", False),
                }
        
        return {
            "success": True,
            "outputs": results,
        }
    
    async def _observe(self, execution_result: Dict) -> Dict[str, Any]:
        """
        Observe and interpret execution results.
        
        Returns observation with:
        - changes: What changed
        - new_state: Updated state
        - unexpected: Unexpected outcomes
        """
        observation = {
            "execution_success": execution_result.get("success", False),
            "changes": [],
            "new_state": self._get_current_state(),
            "unexpected": [],
        }
        
        # Detect changes
        if self.context.get("last_analysis"):
            old_state = self.context["last_analysis"].get("current_state", {})
            new_state = observation["new_state"]
            observation["changes"] = self._detect_changes(old_state, new_state)
        
        # Check for unexpected outcomes
        if execution_result.get("success"):
            expected = self.context.get("last_plan", {}).get("estimated_impact", {})
            observation["unexpected"] = self._find_unexpected(expected, execution_result)
        
        self.context["last_observation"] = observation
        return observation
    
    async def _learn(self, observation: Dict) -> Dict[str, Any]:
        """
        Learn from observation and update knowledge.
        
        Returns learning with:
        - insights: What was learned
        - adjustments: Adjustments to make
        - patterns: Patterns detected
        """
        learning = {
            "insights": [],
            "adjustments": [],
            "patterns": [],
        }
        
        # Extract insights from observation
        if observation.get("unexpected"):
            learning["insights"].extend([
                f"Unexpected: {u}" for u in observation["unexpected"]
            ])
        
        # Detect patterns from step history
        if len(self.step_results) >= 3:
            learning["patterns"] = self._detect_patterns(self.step_results)
        
        # Determine adjustments
        if not observation.get("execution_success"):
            learning["adjustments"].append({
                "type": "retry_strategy",
                "suggestion": "Try alternative approach",
            })
        
        # Store learnings
        if learning["insights"] or learning["patterns"]:
            self.learnings.append(learning)
            self.metrics.learnings_count += 1
            
            # Callback
            if self.on_learning:
                await self._safe_callback(self.on_learning, learning)
        
        self.context["last_learning"] = learning
        return learning
    
    # Helper methods
    
    def _get_current_state(self) -> Dict[str, Any]:
        """Get current execution state."""
        return {
            "steps_completed": self.current_step,
            "context_keys": list(self.context.keys()),
            "has_learnings": len(self.learnings) > 0,
            "agent_status": getattr(self.agent, "status", "unknown"),
        }
    
    def _get_goal_state(self) -> Dict[str, Any]:
        """Get goal state from task."""
        return {
            "task_completed": True,
            "task_name": self.task.name,
            "task_description": self.task.description,
        }
    
    def _identify_gaps(self, current: Dict, goal: Dict) -> List[Dict]:
        """Identify gaps between current and goal state."""
        gaps = []
        
        # Check if task is complete
        if not current.get("has_learnings"):
            gaps.append({
                "type": "execution",
                "description": f"Need to execute: {self.task.name}",
                "priority": 10,
            })
        
        return gaps
    
    def _gap_to_action(self, gap: Dict) -> Optional[Dict]:
        """Convert a gap to an actionable step."""
        gap_type = gap.get("type")
        
        if gap_type == "execution":
            return {
                "type": "execute_task",
                "task_name": self.task.name,
                "priority": gap.get("priority", 5),
            }
        
        return None
    
    def _calculate_priority(self, gaps: List[Dict]) -> int:
        """Calculate overall priority."""
        if not gaps:
            return 0
        return max(g.get("priority", 0) for g in gaps)
    
    def _estimate_impact(self, actions: List[Dict]) -> Dict:
        """Estimate impact of actions."""
        return {
            "expected_progress": len(actions),
            "confidence": 0.8,
        }
    
    async def _execute_action(self, action: Dict) -> Dict[str, Any]:
        """Execute a single action."""
        action_type = action.get("type")
        
        if action_type == "execute_task":
            # Execute via agent
            return await self.agent.execute_task(self.task)
        
        return {"success": False, "error": f"Unknown action type: {action_type}"}
    
    def _detect_changes(self, old_state: Dict, new_state: Dict) -> List[Dict]:
        """Detect changes between states."""
        changes = []
        
        if old_state.get("steps_completed", 0) != new_state.get("steps_completed", 0):
            changes.append({
                "type": "progress",
                "description": f"Step {new_state.get('steps_completed')} completed",
            })
        
        return changes
    
    def _find_unexpected(self, expected: Dict, result: Dict) -> List[str]:
        """Find unexpected outcomes."""
        unexpected = []
        
        # Add domain-specific unexpected detection
        if result.get("error"):
            unexpected.append(f"Error occurred: {result['error']}")
        
        return unexpected
    
    def _detect_patterns(self, steps: List[StepResult]) -> List[Dict]:
        """Detect patterns from step history."""
        patterns = []
        
        # Check for repeated failures
        failures = [s for s in steps if not s.success]
        if len(failures) >= 2:
            patterns.append({
                "type": "repeated_failures",
                "count": len(failures),
                "suggestion": "Consider alternative approach",
            })
        
        return patterns
    
    async def _safe_callback(self, callback: Callable, data: Any) -> None:
        """Safely execute a callback."""
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(data)
            else:
                callback(data)
        except Exception:
            pass  # Don't fail on callback errors
    
    def _build_result(self) -> Dict[str, Any]:
        """Build final result."""
        return {
            "success": self.state == LoopState.COMPLETED,
            "state": self.state.value,
            "total_steps": self.current_step,
            "metrics": self.metrics.model_dump(),
            "step_results": [r.model_dump() for r in self.step_results],
            "learnings": self.learnings,
            "context": self.context,
        }