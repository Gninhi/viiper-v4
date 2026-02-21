"""
Enhanced Orchestrator with sub-agent spawning and parallel execution.

Extends ProjectOrchestrator with advanced capabilities:
- Sub-agent spawning for complex tasks
- Parallel task execution
- Enhanced error recovery
- Integration with IterativeAgentLoop
"""

from typing import List, Dict, Any, Optional, Set
from pydantic import BaseModel, Field
from datetime import datetime
import asyncio
import time

from viiper.core.project import Project
from viiper.core.phase import Phase
from viiper.agents.base import Agent, AgentTask, AgentRole, AgentCapability
from viiper.agents.factory import AgentFactory
from viiper.agents.collaboration import CollaborationProtocol, MessageType, SharedContext
from viiper.orchestrator.project_orchestrator import ProjectOrchestrator, OrchestrationResult
from viiper.orchestrator.iterative_loop import IterativeAgentLoop, LoopState


class SubAgentSpawner:
    """
    Handles spawning and management of sub-agents.
    
    Inspired by Manus AI architecture for hierarchical agent execution.
    """
    
    def __init__(self, max_sub_agents: int = 10):
        """
        Initialize spawner.
        
        Args:
            max_sub_agents: Maximum concurrent sub-agents
        """
        self.max_sub_agents = max_sub_agents
        self.active_sub_agents: Dict[str, Agent] = {}
        self.sub_agent_count = 0
    
    def spawn_agent(self, agent_type: str, parent_id: str) -> Optional[Agent]:
        """
        Spawn a new sub-agent.
        
        Args:
            agent_type: Type of agent to spawn
            parent_id: ID of parent agent/orchestrator
            
        Returns:
            Spawned agent or None if limit reached
        """
        if len(self.active_sub_agents) >= self.max_sub_agents:
            return None
        
        agent = AgentFactory.create_agent(agent_type)
        if agent:
            self.sub_agent_count += 1
            sub_agent_id = f"sub_{agent_type}_{self.sub_agent_count}"
            self.active_sub_agents[sub_agent_id] = agent
            return agent
        
        return None
    
    def release_agent(self, agent_id: str) -> None:
        """Release a sub-agent."""
        if agent_id in self.active_sub_agents:
            del self.active_sub_agents[agent_id]
    
    def get_active_count(self) -> int:
        """Get number of active sub-agents."""
        return len(self.active_sub_agents)


class ParallelExecutor:
    """
    Executes tasks in parallel with concurrency control.
    """
    
    def __init__(self, max_concurrent: int = 5):
        """
        Initialize executor.
        
        Args:
            max_concurrent: Maximum concurrent tasks
        """
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def execute_parallel(
        self,
        tasks: List[AgentTask],
        agents: List[Agent],
    ) -> List[Dict[str, Any]]:
        """
        Execute multiple tasks in parallel.
        
        Args:
            tasks: Tasks to execute
            agents: Available agents
            
        Returns:
            List of results
        """
        async def execute_with_semaphore(task: AgentTask) -> Dict[str, Any]:
            async with self.semaphore:
                # Find capable agent
                agent = self._find_agent_for_task(task, agents)
                if not agent:
                    return {
                        "task_id": task.id,
                        "success": False,
                        "error": f"No agent available for task: {task.name}",
                    }
                
                agent.assign_task(task)
                result = await agent.execute_task(task)
                agent.complete_task(result)
                return result
        
        # Execute all tasks concurrently
        results = await asyncio.gather(
            *[execute_with_semaphore(task) for task in tasks],
            return_exceptions=True,
        )
        
        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "task_id": tasks[i].id,
                    "success": False,
                    "error": str(result),
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    def _find_agent_for_task(self, task: AgentTask, agents: List[Agent]) -> Optional[Agent]:
        """Find an available agent for a task."""
        for agent in agents:
            if agent.status == "idle":
                return agent
        return None


class ErrorRecovery:
    """
    Handles error recovery and retry logic.
    """
    
    def __init__(self, max_retries: int = 3, backoff_factor: float = 2.0):
        """
        Initialize recovery handler.
        
        Args:
            max_retries: Maximum retry attempts
            backoff_factor: Exponential backoff factor
        """
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
    
    async def execute_with_retry(
        self,
        task: AgentTask,
        agent: Agent,
        on_retry: Optional[callable] = None,
    ) -> Dict[str, Any]:
        """
        Execute task with automatic retry.
        
        Args:
            task: Task to execute
            agent: Agent to execute with
            on_retry: Callback on retry
            
        Returns:
            Execution result
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                agent.assign_task(task)
                result = await agent.execute_task(task)
                
                if result.get("success", False):
                    agent.complete_task(result)
                    return result
                
                last_error = result.get("error", "Unknown error")
                
                # Call retry callback
                if on_retry and attempt < self.max_retries - 1:
                    await on_retry(task, agent, attempt, last_error)
                
                # Backoff
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.backoff_factor ** attempt)
                    
            except Exception as e:
                last_error = str(e)
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.backoff_factor ** attempt)
        
        # All retries failed
        agent.fail_task(last_error or "Max retries exceeded")
        return {
            "task_id": task.id,
            "success": False,
            "error": last_error,
            "retries": self.max_retries,
        }


class EnhancedOrchestrator(ProjectOrchestrator):
    """
    Enhanced orchestrator with advanced capabilities.
    
    Features:
    - Sub-agent spawning for complex tasks
    - Parallel task execution
    - Error recovery with retries
    - Integration with IterativeAgentLoop
    - Browse → Idea → Code pipeline support
    """
    
    def __init__(
        self,
        project: Project,
        max_sub_agents: int = 10,
        max_parallel_tasks: int = 5,
        auto_register_agents: bool = True,
    ):
        """
        Initialize enhanced orchestrator.
        
        Args:
            project: Project to orchestrate
            max_sub_agents: Maximum concurrent sub-agents
            max_parallel_tasks: Maximum parallel tasks
            auto_register_agents: Auto-register all agents
        """
        super().__init__(project, auto_register_agents)
        
        # Enhanced components
        self.spawner = SubAgentSpawner(max_sub_agents)
        self.parallel_executor = ParallelExecutor(max_parallel_tasks)
        self.error_recovery = ErrorRecovery()
        
        # Iterative loop tracking
        self.active_loops: Dict[str, IterativeAgentLoop] = {}
        
        # Pipeline mode for Browse → Idea → Code
        self.pipeline_mode = False
        self.pipeline_stage = None
    
    async def execute_phase_enhanced(
        self,
        phase: Optional[Phase] = None,
        parallel: bool = True,
        use_iterative_loop: bool = True,
    ) -> OrchestrationResult:
        """
        Execute phase with enhanced capabilities.
        
        Args:
            phase: Phase to execute
            parallel: Enable parallel execution
            use_iterative_loop: Use iterative loop for complex tasks
            
        Returns:
            Orchestration result
        """
        start_time = time.time()
        target_phase = phase or self.project.phase
        
        # Update context
        self.context.phase = target_phase.value
        
        # Generate tasks
        tasks = self._generate_phase_tasks(target_phase)
        
        # Categorize tasks
        parallel_tasks = []
        sequential_tasks = []
        
        for task in tasks:
            if task.priority >= 9 and parallel:
                parallel_tasks.append(task)
            else:
                sequential_tasks.append(task)
        
        results = []
        errors = []
        
        # Execute parallel tasks
        if parallel_tasks:
            parallel_results = await self.parallel_executor.execute_parallel(
                parallel_tasks, self.agents
            )
            results.extend(parallel_results)
            errors.extend([r.get("error") for r in parallel_results if not r.get("success")])
        
        # Execute sequential tasks with iterative loop
        for task in sequential_tasks:
            try:
                agent = self.find_capable_agent(task)
                if not agent:
                    errors.append(f"No agent for task: {task.name}")
                    continue
                
                if use_iterative_loop:
                    # Use iterative loop for complex tasks
                    result = await self._execute_with_loop(agent, task)
                else:
                    # Standard execution
                    result = await self._execute_with_retry(agent, task)
                
                results.append(result)
                
                if not result.get("success"):
                    errors.append(result.get("error", f"Task {task.name} failed"))
                
                # Share context
                self.collaboration.share_context(self.project.id, agent.name, result)
                
            except Exception as e:
                errors.append(f"Task {task.name} error: {str(e)}")
        
        duration = time.time() - start_time
        
        return OrchestrationResult(
            success=len(errors) == 0,
            phase=target_phase,
            tasks_completed=len([r for r in results if r.get("success")]),
            tasks_failed=len(errors),
            results=results,
            errors=errors,
            duration_seconds=duration,
        )
    
    async def _execute_with_loop(self, agent: Agent, task: AgentTask) -> Dict[str, Any]:
        """Execute task using iterative loop."""
        loop = IterativeAgentLoop(
            agent=agent,
            task=task,
            max_steps=IterativeAgentLoop.ORCHESTRATOR_MAX_STEPS,
            on_step_complete=self._on_step_complete,
            on_learning=self._on_learning,
        )
        
        self.active_loops[task.id] = loop
        result = await loop.run()
        del self.active_loops[task.id]
        
        return result
    
    async def _execute_with_retry(self, agent: Agent, task: AgentTask) -> Dict[str, Any]:
        """Execute task with retry logic."""
        return await self.error_recovery.execute_with_retry(
            task, agent, on_retry=self._on_retry
        )
    
    async def spawn_and_execute(
        self,
        agent_type: str,
        task: AgentTask,
    ) -> Dict[str, Any]:
        """
        Spawn a sub-agent and execute a task.
        
        Args:
            agent_type: Type of agent to spawn
            task: Task for sub-agent
            
        Returns:
            Execution result
        """
        sub_agent = self.spawner.spawn_agent(agent_type, self.project.id)
        if not sub_agent:
            return {
                "success": False,
                "error": "Maximum sub-agents reached",
            }
        
        try:
            # Execute with higher step limit for sub-agents
            loop = IterativeAgentLoop(
                agent=sub_agent,
                task=task,
                max_steps=IterativeAgentLoop.SUB_AGENT_MAX_STEPS,
            )
            result = await loop.run()
            return result
        finally:
            # Release sub-agent
            self.spawner.release_agent(sub_agent.name)
    
    async def execute_browse_idea_code_pipeline(
        self,
        niche: str = "",
        max_ideas: int = 5,
    ) -> Dict[str, Any]:
        """
        Execute the Browse → Idea → Code pipeline.
        
        Args:
            niche: Target niche for ideas
            max_ideas: Maximum ideas to generate
            
        Returns:
            Pipeline results
        """
        self.pipeline_mode = True
        pipeline_results = {
            "discovery": {},
            "ideation": {},
            "production": {},
        }
        
        # Phase 1: Discovery (Browse + Idea Generation)
        self.pipeline_stage = "discovery"
        
        # Spawn BrowserAgent for research
        browse_task = AgentTask(
            name="Browse Trends",
            description=f"Research trends in {niche}",
            metadata={"type": "search", "query": f"{niche} startup ideas trends 2026"} if niche else {},
        )
        
        browse_result = await self.spawn_and_execute("browser", browse_task)
        pipeline_results["discovery"]["browse"] = browse_result
        
        # Spawn IdeaGenerationAgent
        idea_task = AgentTask(
            name="Generate Ideas",
            description="Generate and score app ideas",
            metadata={
                "niche": niche,
                "max_ideas": max_ideas,
                "min_score": 0.6,
            },
        )
        
        idea_result = await self.spawn_and_execute("idea_generation", idea_task)
        pipeline_results["discovery"]["ideas"] = idea_result
        
        # Phase 2: Ideation (if ideas found)
        if idea_result.get("success") and idea_result.get("data", {}).get("ideas"):
            self.pipeline_stage = "ideation"
            
            top_idea = idea_result["data"]["top_recommendation"]
            
            # Create architecture for top idea
            arch_task = AgentTask(
                name="System Architecture",
                description=f"Design architecture for: {top_idea.get('title', 'Selected Idea')}",
                context={"idea": top_idea},
            )
            
            arch_result = await self.spawn_and_execute("system_design", arch_task)
            pipeline_results["ideation"]["architecture"] = arch_result
            
            # Tech stack selection
            tech_task = AgentTask(
                name="Tech Stack Selection",
                description="Select optimal tech stack",
                context={"architecture": arch_result.get("data")},
            )
            
            tech_result = await self.spawn_and_execute("tech_stack", tech_task)
            pipeline_results["ideation"]["tech_stack"] = tech_result
        
        # Phase 3: Production (scaffold project)
        self.pipeline_stage = "production"
        
        # Execute production phase with parallel tasks
        production_result = await self.execute_phase_enhanced(
            phase=Phase.PRODUCTION,
            parallel=True,
        )
        pipeline_results["production"] = production_result.model_dump()
        
        self.pipeline_mode = False
        return pipeline_results
    
    # Callbacks
    
    async def _on_step_complete(self, step_result: Dict) -> None:
        """Handle step completion."""
        # Could emit events, update UI, etc.
        pass
    
    async def _on_learning(self, learning: Dict) -> None:
        """Handle learning event."""
        # Could store in CKB, emit events, etc.
        pass
    
    async def _on_retry(self, task: AgentTask, agent: Agent, attempt: int, error: str) -> None:
        """Handle retry event."""
        # Could log, notify, etc.
        pass
    
    def get_enhanced_status(self) -> Dict[str, Any]:
        """Get enhanced orchestrator status."""
        base_status = self.get_status()
        
        base_status.update({
            "sub_agents_active": self.spawner.get_active_count(),
            "parallel_tasks_capacity": self.parallel_executor.max_concurrent,
            "active_loops": len(self.active_loops),
            "pipeline_mode": self.pipeline_mode,
            "pipeline_stage": self.pipeline_stage,
        })
        
        return base_status