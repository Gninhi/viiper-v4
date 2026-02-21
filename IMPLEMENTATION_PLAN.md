# VIIPER V4 - Plan d'Implémentation Complet
## Objectif: Browse → Idea → Code (End-to-End Autonomous Development)

**Version**: v0.2.0
**Date**: 21/02/2026
**Durée estimée**: 7 semaines

---

## 📋 Vue d'Ensemble du Plan

```
Semaine 1-2: Foundation Layer
├── BrowserAgent (Playwright)
├── IterativeAgentLoop
└── Tests unitaires

Semaine 3-4: Intelligence Layer
├── IdeaGenerationAgent
├── Enhanced Orchestrator
└── Sub-agent Spawning

Semaine 5-6: Integration Layer
├── End-to-End Workflow
├── Context Sharing
└── Error Recovery

Semaine 7: Polish & Demo
├── Quality Gates
├── Documentation
└── Demo Project
```

---

## 🎯 Phase 1: Foundation Layer (Semaines 1-2)

### Sprint 1.1: BrowserAgent

#### 1.1.1 Créer le fichier agent

**Fichier**: `viiper/agents/browser.py`

```python
"""
Browser Agent for autonomous web navigation.

Enables VIIPER to browse the web, scrape content, and interact with pages.
"""

from typing import Dict, Any, List, Optional
from viiper.agents.base import Agent, AgentRole, AgentCapability, AgentTask
from playwright.async_api import async_playwright, Browser, Page
import asyncio
from datetime import datetime


class BrowserCapability(AgentCapability):
    """Extended capabilities for browser operations."""
    WEB_NAVIGATION = "web_navigation"
    CONTENT_SCRAPING = "content_scraping"
    SCREENSHOT_CAPTURE = "screenshot_capture"
    FORM_INTERACTION = "form_interaction"
    SEARCH = "search"


class BrowserAgent(Agent):
    """
    Agent specialized in autonomous web navigation.
    
    Capabilities:
    - Navigate to URLs
    - Scrape content from pages
    - Capture screenshots
    - Fill forms and click elements
    - Perform web searches
    - Extract structured data
    
    Inspired by: Manus AI browser integration
    """
    
    name: str = "Browser Agent"
    role: AgentRole = AgentRole.SPECIALIST
    capabilities: List[AgentCapability] = [
        BrowserCapability.WEB_NAVIGATION,
        BrowserCapability.CONTENT_SCRAPING,
        BrowserCapability.SCREENSHOT_CAPTURE,
        BrowserCapability.FORM_INTERACTION,
        BrowserCapability.SEARCH,
    ]
    
    # Browser state
    _playwright = None
    _browser: Optional[Browser] = None
    _page: Optional[Page] = None
    _session_history: List[Dict] = []
    
    async def setup(self) -> None:
        """Initialize browser session."""
        if self._browser is None:
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            self._page = await self._browser.new_page()
    
    async def teardown(self) -> None:
        """Close browser session."""
        if self._browser:
            await self._browser.close()
            self._browser = None
            self._page = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None
    
    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute browser-related task.
        
        Task types:
        - navigate: Go to URL
        - scrape: Extract content
        - screenshot: Capture page
        - search: Web search
        - interact: Click, type, fill
        """
        await self.setup()
        
        task_type = task.metadata.get("type", "navigate")
        
        try:
            if task_type == "navigate":
                result = await self._navigate(task.metadata.get("url"))
            elif task_type == "scrape":
                result = await self._scrape(task.metadata)
            elif task_type == "screenshot":
                result = await self._screenshot(task.metadata.get("full_page", True))
            elif task_type == "search":
                result = await self._search(task.metadata.get("query"))
            elif task_type == "interact":
                result = await self._interact(task.metadata)
            elif task_type == "extract":
                result = await self._extract_structured(task.metadata)
            else:
                result = {"error": f"Unknown task type: {task_type}"}
            
            # Log to session history
            self._session_history.append({
                "timestamp": datetime.now().isoformat(),
                "task_type": task_type,
                "result_summary": {k: v for k, v in result.items() if k != "raw_content"}
            })
            
            return {
                "task_id": task.id,
                "task_name": task.name,
                "success": True,
                "data": result
            }
            
        except Exception as e:
            return {
                "task_id": task.id,
                "task_name": task.name,
                "success": False,
                "error": str(e)
            }
    
    async def _navigate(self, url: str) -> Dict[str, Any]:
        """Navigate to URL."""
        await self._page.goto(url, wait_until="networkidle")
        
        return {
            "url": self._page.url,
            "title": await self._page.title(),
            "status": "success"
        }
    
    async def _scrape(self, metadata: Dict) -> Dict[str, Any]:
        """Scrape content from page."""
        selector = metadata.get("selector", "body")
        extract_links = metadata.get("extract_links", False)
        extract_images = metadata.get("extract_images", False)
        
        # Get text content
        elements = await self._page.query_selector_all(selector)
        texts = [await el.text_content() for el in elements]
        
        result = {
            "content": "\n".join([t for t in texts if t]),
            "url": self._page.url,
        }
        
        if extract_links:
            links = await self._page.query_selector_all("a[href]")
            result["links"] = [
                {"text": await l.text_content(), "href": await l.get_attribute("href")}
                for l in links
            ]
        
        if extract_images:
            images = await self._page.query_selector_all("img[src]")
            result["images"] = [
                {"alt": await i.get_attribute("alt"), "src": await i.get_attribute("src")}
                for i in images
            ]
        
        return result
    
    async def _screenshot(self, full_page: bool = True) -> Dict[str, Any]:
        """Capture screenshot."""
        screenshot_bytes = await self._page.screenshot(full_page=full_page)
        
        import base64
        screenshot_base64 = base64.b64encode(screenshot_bytes).decode()
        
        return {
            "screenshot": screenshot_base64,
            "url": self._page.url,
            "full_page": full_page
        }
    
    async def _search(self, query: str) -> Dict[str, Any]:
        """Perform web search."""
        # Use DuckDuckGo for privacy
        search_url = f"https://duckduckgo.com/?q={query}"
        await self._page.goto(search_url)
        
        # Wait for results
        await self._page.wait_for_selector('[data-testid="result"]', timeout=10000)
        
        # Extract results
        results = await self._page.query_selector_all('[data-testid="result"]')
        
        search_results = []
        for result in results[:10]:  # Top 10
            title_el = await result.query_selector("h2")
            link_el = await result.query_selector("a[href]")
            snippet_el = await result.query_selector('[data-testid="result-snippet"]')
            
            if title_el and link_el:
                search_results.append({
                    "title": await title_el.text_content(),
                    "url": await link_el.get_attribute("href"),
                    "snippet": await snippet_el.text_content() if snippet_el else ""
                })
        
        return {
            "query": query,
            "results": search_results,
            "count": len(search_results)
        }
    
    async def _interact(self, metadata: Dict) -> Dict[str, Any]:
        """Interact with page elements."""
        action = metadata.get("action", "click")
        selector = metadata.get("selector")
        text = metadata.get("text", "")
        
        if action == "click":
            await self._page.click(selector)
        elif action == "type":
            await self._page.fill(selector, text)
        elif action == "press":
            await self._page.press(selector, text)
        
        return {
            "action": action,
            "selector": selector,
            "status": "success"
        }
    
    async def _extract_structured(self, metadata: Dict) -> Dict[str, Any]:
        """Extract structured data using selectors."""
        schema = metadata.get("schema", {})
        results = []
        
        for field_name, selector in schema.items():
            elements = await self._page.query_selector_all(selector)
            values = [await el.text_content() for el in elements]
            results.append({field_name: values})
        
        return {"extracted": results}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get browser agent statistics."""
        base_stats = super().get_stats()
        base_stats["browser"] = {
            "session_active": self._browser is not None,
            "pages_visited": len(self._session_history),
            "last_visit": self._session_history[-1] if self._session_history else None
        }
        return base_stats
```

#### 1.1.2 Ajouter les dépendances

**Fichier**: `requirements.txt` (ajouter)

```
playwright>=1.40.0
```

#### 1.1.3 Enregistrer l'agent

**Fichier**: `viiper/agents/__init__.py` (modifier)

```python
from viiper.agents.browser import BrowserAgent

# Ajouter à AGENT_CLASSES
AGENT_CLASSES = {
    # ... existing agents ...
    "browser": BrowserAgent,
}

# Ajouter à AGENTS_BY_ROLE
AGENTS_BY_ROLE = {
    # ... existing mappings ...
    AgentRole.SPECIALIST: ["seo", "content_writer", "browser"],
}

# Ajouter à AGENTS_BY_CAPABILITY
AGENTS_BY_CAPABILITY = {
    # ... existing mappings ...
    BrowserCapability.WEB_NAVIGATION: ["browser"],
    BrowserCapability.CONTENT_SCRAPING: ["browser"],
    BrowserCapability.SEARCH: ["browser"],
}
```

#### 1.1.4 Tests unitaires

**Fichier**: `tests/unit/test_browser_agent.py`

```python
"""Tests for BrowserAgent."""

import pytest
from viiper.agents.browser import BrowserAgent, BrowserCapability
from viiper.agents.base import AgentTask


@pytest.fixture
async def browser_agent():
    agent = BrowserAgent()
    yield agent
    await agent.teardown()


@pytest.mark.asyncio
async def test_browser_agent_navigate(browser_agent):
    task = AgentTask(
        name="Navigate",
        description="Navigate to example.com",
        metadata={"type": "navigate", "url": "https://example.com"}
    )
    
    result = await browser_agent.execute_task(task)
    
    assert result["success"] is True
    assert "example.com" in result["data"]["url"]


@pytest.mark.asyncio
async def test_browser_agent_scrape(browser_agent):
    # First navigate
    nav_task = AgentTask(
        name="Navigate",
        metadata={"type": "navigate", "url": "https://example.com"}
    )
    await browser_agent.execute_task(nav_task)
    
    # Then scrape
    scrape_task = AgentTask(
        name="Scrape",
        metadata={"type": "scrape", "selector": "h1"}
    )
    
    result = await browser_agent.execute_task(scrape_task)
    
    assert result["success"] is True
    assert len(result["data"]["content"]) > 0


@pytest.mark.asyncio
async def test_browser_agent_search(browser_agent):
    task = AgentTask(
        name="Search",
        description="Search for Python",
        metadata={"type": "search", "query": "Python programming"}
    )
    
    result = await browser_agent.execute_task(task)
    
    assert result["success"] is True
    assert len(result["data"]["results"]) > 0
```

---

### Sprint 1.2: IterativeAgentLoop

#### 1.2.1 Créer le module core

**Fichier**: `viiper/core/iterative_loop.py`

```python
"""
Iterative Agent Loop for autonomous execution.

Implements the Analyze → Plan → Execute → Observe → Learn cycle
inspired by Manus AI architecture.
"""

from typing import Dict, Any, List, Optional, Callable
from pydantic import BaseModel, Field
from enum import Enum
import asyncio
from datetime import datetime


class LoopState(str, Enum):
    """States in the iterative loop."""
    IDLE = "idle"
    ANALYZING = "analyzing"
    PLANNING = "planning"
    EXECUTING = "executing"
    OBSERVING = "observing"
    LEARNING = "learning"
    COMPLETE = "complete"
    FAILED = "failed"


class IterationResult(BaseModel):
    """Result of a single iteration."""
    iteration: int
    state: LoopState
    analysis: Optional[Dict[str, Any]] = None
    plan: Optional[Dict[str, Any]] = None
    execution: Optional[Dict[str, Any]] = None
    observation: Optional[Dict[str, Any]] = None
    learning: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class LoopOutcome(BaseModel):
    """Final outcome of the loop."""
    success: bool
    iterations: int
    results: List[IterationResult]
    final_output: Dict[str, Any]
    duration_seconds: float
    lessons_learned: List[str] = Field(default_factory=list)


class IterativeAgentLoop:
    """
    Implements autonomous iterative execution.
    
    Cycle:
    1. ANALYZE: Assess current state and goal
    2. PLAN: Determine next actions
    3. EXECUTE: Perform actions
    4. OBSERVE: Monitor results
    5. LEARN: Extract insights
    
    Inspired by Manus AI's iterative agent architecture.
    """
    
    def __init__(
        self,
        max_iterations: int = 50,
        convergence_threshold: float = 0.95,
        timeout_seconds: int = 300,
        on_iteration: Optional[Callable] = None
    ):
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        self.timeout_seconds = timeout_seconds
        self.on_iteration = on_iteration
        
        self.state = LoopState.IDLE
        self.current_iteration = 0
        self.history: List[IterationResult] = []
    
    async def run(
        self,
        goal: str,
        context: Dict[str, Any],
        executor: Callable,
        analyzer: Optional[Callable] = None,
        planner: Optional[Callable] = None,
        observer: Optional[Callable] = None,
        learner: Optional[Callable] = None
    ) -> LoopOutcome:
        """
        Run the iterative loop until goal is achieved or max iterations.
        
        Args:
            goal: The objective to achieve
            context: Initial context/state
            executor: Function to execute actions
            analyzer: Optional custom analyzer
            planner: Optional custom planner
            observer: Optional custom observer
            learner: Optional custom learner
        
        Returns:
            LoopOutcome with results
        """
        import time
        start_time = time.time()
        
        current_context = context.copy()
        lessons = []
        
        while self.current_iteration < self.max_iterations:
            self.current_iteration += 1
            iteration_result = IterationResult(
                iteration=self.current_iteration,
                state=self.state
            )
            
            try:
                # ANALYZE
                self.state = LoopState.ANALYZING
                analysis = await self._analyze(
                    goal, current_context, analyzer
                )
                iteration_result.analysis = analysis
                
                # Check convergence
                if analysis.get("completion_score", 0) >= self.convergence_threshold:
                    self.state = LoopState.COMPLETE
                    break
                
                # PLAN
                self.state = LoopState.PLANNING
                plan = await self._plan(
                    goal, analysis, current_context, planner
                )
                iteration_result.plan = plan
                
                if not plan.get("actions"):
                    # No more actions to take
                    self.state = LoopState.COMPLETE
                    break
                
                # EXECUTE
                self.state = LoopState.EXECUTING
                execution = await self._execute(
                    plan, executor, current_context
                )
                iteration_result.execution = execution
                
                # OBSERVE
                self.state = LoopState.OBSERVING
                observation = await self._observe(
                    execution, current_context, observer
                )
                iteration_result.observation = observation
                
                # Update context
                current_context.update(observation.get("context_updates", {}))
                
                # LEARN
                self.state = LoopState.LEARNING
                learning = await self._learn(
                    iteration_result, current_context, learner
                )
                iteration_result.learning = learning
                
                if learning.get("lessons"):
                    lessons.extend(learning["lessons"])
                
                self.history.append(iteration_result)
                
                # Callback for progress tracking
                if self.on_iteration:
                    await self.on_iteration(iteration_result)
                
                # Check for timeout
                if time.time() - start_time > self.timeout_seconds:
                    self.state = LoopState.FAILED
                    break
                    
            except Exception as e:
                iteration_result.observation = {"error": str(e)}
                self.history.append(iteration_result)
                # Continue to next iteration with error info
                current_context["last_error"] = str(e)
        
        duration = time.time() - start_time
        
        return LoopOutcome(
            success=self.state == LoopState.COMPLETE,
            iterations=self.current_iteration,
            results=self.history,
            final_output=current_context,
            duration_seconds=duration,
            lessons_learned=lessons
        )
    
    async def _analyze(
        self,
        goal: str,
        context: Dict,
        custom_analyzer: Optional[Callable]
    ) -> Dict[str, Any]:
        """Analyze current state relative to goal."""
        if custom_analyzer:
            return await custom_analyzer(goal, context)
        
        # Default analysis
        return {
            "goal": goal,
            "current_state": context.get("current_state", "unknown"),
            "completion_score": context.get("completion_score", 0.0),
            "blockers": context.get("blockers", []),
            "next_steps": context.get("suggested_actions", [])
        }
    
    async def _plan(
        self,
        goal: str,
        analysis: Dict,
        context: Dict,
        custom_planner: Optional[Callable]
    ) -> Dict[str, Any]:
        """Plan next actions based on analysis."""
        if custom_planner:
            return await custom_planner(goal, analysis, context)
        
        # Default planning
        return {
            "actions": analysis.get("next_steps", []),
            "priority": "high" if analysis.get("completion_score", 0) < 0.5 else "medium"
        }
    
    async def _execute(
        self,
        plan: Dict,
        executor: Callable,
        context: Dict
    ) -> Dict[str, Any]:
        """Execute planned actions."""
        results = []
        
        for action in plan.get("actions", []):
            result = await executor(action, context)
            results.append(result)
        
        return {
            "actions_executed": len(results),
            "results": results
        }
    
    async def _observe(
        self,
        execution: Dict,
        context: Dict,
        custom_observer: Optional[Callable]
    ) -> Dict[str, Any]:
        """Observe results of execution."""
        if custom_observer:
            return await custom_observer(execution, context)
        
        # Default observation
        return {
            "success": all(r.get("success", False) for r in execution.get("results", [])),
            "context_updates": {
                "last_execution": execution,
                "execution_count": context.get("execution_count", 0) + 1
            }
        }
    
    async def _learn(
        self,
        iteration: IterationResult,
        context: Dict,
        custom_learner: Optional[Callable]
    ) -> Dict[str, Any]:
        """Learn from iteration results."""
        if custom_learner:
            return await custom_learner(iteration, context)
        
        # Default learning
        lessons = []
        
        if iteration.observation and not iteration.observation.get("success"):
            lessons.append(f"Iteration {iteration.iteration}: Execution failed, consider alternative approach")
        
        return {"lessons": lessons}
    
    def reset(self) -> None:
        """Reset the loop state."""
        self.state = LoopState.IDLE
        self.current_iteration = 0
        self.history = []
```

---

### Sprint 1.3: Step Limits & Resource Management

#### 1.3.1 Créer le module de gestion des ressources

**Fichier**: `viiper/core/resource_manager.py`

```python
"""
Resource management for agent execution.

Implements step limits inspired by Kimi K2.5:
- Orchestrator: 15 steps max
- Sub-agents: 100 steps max
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
import asyncio


class ResourceType(str, Enum):
    """Types of resources to manage."""
    STEPS = "steps"
    TIME = "time"
    TOKENS = "tokens"
    BROWSER_SESSIONS = "browser_sessions"


class ResourceLimits(BaseModel):
    """Limits for resource consumption."""
    max_steps: int = 100
    max_time_seconds: int = 300
    max_tokens: int = 100000
    max_browser_sessions: int = 5
    
    # Current usage
    steps_used: int = 0
    time_used_seconds: float = 0.0
    tokens_used: int = 0
    browser_sessions: int = 0


class ResourceManager:
    """
    Manages resource consumption for agents.
    
    Inspired by Kimi K2.5 step limits:
    - Orchestrator agents: 15 steps
    - Sub-agents: 100 steps
    """
    
    # Default limits by agent type
    DEFAULT_LIMITS = {
        "orchestrator": ResourceLimits(max_steps=15, max_time_seconds=600),
        "sub_agent": ResourceLimits(max_steps=100, max_time_seconds=300),
        "browser": ResourceLimits(max_steps=200, max_time_seconds=600),
        "standard": ResourceLimits(max_steps=50, max_time_seconds=300),
    }
    
    def __init__(self, agent_type: str = "standard"):
        self.agent_type = agent_type
        self.limits = self.DEFAULT_LIMITS.get(agent_type, ResourceLimits()).copy()
        self.start_time = datetime.now()
    
    def can_execute(self) -> bool:
        """Check if execution is still allowed."""
        # Check steps
        if self.limits.steps_used >= self.limits.max_steps:
            return False
        
        # Check time
        elapsed = (datetime.now() - self.start_time).total_seconds()
        if elapsed >= self.limits.max_time_seconds:
            return False
        
        return True
    
    def increment_step(self) -> None:
        """Increment step counter."""
        self.limits.steps_used += 1
    
    def get_remaining_steps(self) -> int:
        """Get remaining steps."""
        return max(0, self.limits.max_steps - self.limits.steps_used)
    
    def get_remaining_time(self) -> float:
        """Get remaining time in seconds."""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        return max(0, self.limits.max_time_seconds - elapsed)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current resource status."""
        return {
            "agent_type": self.agent_type,
            "steps": {
                "used": self.limits.steps_used,
                "max": self.limits.max_steps,
                "remaining": self.get_remaining_steps()
            },
            "time": {
                "used": (datetime.now() - self.start_time).total_seconds(),
                "max": self.limits.max_time_seconds,
                "remaining": self.get_remaining_time()
            },
            "can_continue": self.can_execute()
        }


class SubAgentSpawner:
    """
    Spawns and manages sub-agents with resource limits.
    
    Pattern from Kimi K2.5:
    - Orchestrator has 15 steps
    - Each sub-agent has 100 steps
    - Max 10 concurrent sub-agents
    """
    
    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
        self.active_sub_agents: Dict[str, ResourceManager] = {}
    
    async def spawn(
        self,
        agent_id: str,
        agent_factory: Callable,
        task: Any
    ) -> Dict[str, Any]:
        """Spawn a sub-agent with resource limits."""
        # Check capacity
        if len(self.active_sub_agents) >= self.max_concurrent:
            raise RuntimeError(f"Maximum concurrent sub-agents ({self.max_concurrent}) reached")
        
        # Create resource manager for sub-agent
        resource_manager = ResourceManager("sub_agent")
        self.active_sub_agents[agent_id] = resource_manager
        
        try:
            # Create and execute agent
            agent = agent_factory()
            
            # Execute with step tracking
            result = await self._execute_with_limits(agent, task, resource_manager)
            
            return result
            
        finally:
            # Cleanup
            del self.active_sub_agents[agent_id]
    
    async def _execute_with_limits(
        self,
        agent: Any,
        task: Any,
        resource_manager: ResourceManager
    ) -> Dict[str, Any]:
        """Execute agent with step limit enforcement."""
        results = []
        
        while resource_manager.can_execute():
            resource_manager.increment_step()
            
            # Execute one step
            step_result = await agent.execute_step(task)
            results.append(step_result)
            
            # Check if done
            if step_result.get("complete", False):
                break
        
        return {
            "results": results,
            "steps_used": resource_manager.limits.steps_used,
            "resource_status": resource_manager.get_status()
        }
    
    def get_active_count(self) -> int:
        """Get number of active sub-agents."""
        return len(self.active_sub_agents)
    
    def get_all_status(self) -> Dict[str, Any]:
        """Get status of all active sub-agents."""
        return {
            agent_id: rm.get_status()
            for agent_id, rm in self.active_sub_agents.items()
        }


from typing import Callable
```

---

## 🎯 Phase 2: Intelligence Layer (Semaines 3-4)

### Sprint 2.1: IdeaGenerationAgent

#### 2.1.1 Créer l'agent de génération d'idées

**Fichier**: `viiper/agents/idea_generation.py`

```python
"""
Idea Generation Agent for autonomous idea discovery.

Analyzes trends, identifies opportunities, and generates app ideas.
"""

from typing import Dict, Any, List, Optional
from viiper.agents.base import Agent, AgentRole, AgentCapability, AgentTask
from viiper.agents.browser import BrowserAgent
from pydantic import BaseModel, Field
from enum import Enum


class IdeaCategory(str, Enum):
    """Categories of app ideas."""
    SAAS = "saas"
    MARKETPLACE = "marketplace"
    MOBILE_APP = "mobile_app"
    DEV_TOOL = "dev_tool"
    AI_PRODUCT = "ai_product"
    PRODUCTIVITY = "productivity"
    ECOMMERCE = "ecommerce"
    FINTECH = "fintech"
    HEALTH = "health"
    EDUCATION = "education"


class IdeaScore(BaseModel):
    """Scoring for an idea."""
    market_size: float = Field(ge=0, le=1)
    competition: float = Field(ge=0, le=1)  # Lower is better (less competition)
    feasibility: float = Field(ge=0, le=1)
    time_to_mvp: float = Field(ge=0, le=1)  # Higher = faster
    revenue_potential: float = Field(ge=0, le=1)
    overall: float = Field(ge=0, le=1)


class AppIdea(BaseModel):
    """A generated app idea."""
    id: str
    title: str
    description: str
    category: IdeaCategory
    problem: str
    solution: str
    target_audience: str
    key_features: List[str]
    monetization: List[str]
    competitors: List[str]
    score: IdeaScore
    trending_keywords: List[str]


class IdeaGenerationAgent(Agent):
    """
    Agent specialized in generating and validating app ideas.
    
    Workflow:
    1. Browse trending sources (Product Hunt, Twitter, Reddit)
    2. Analyze market patterns
    3. Identify gaps and opportunities
    4. Generate idea candidates
    5. Score and rank ideas
    
    Inspired by: Combines VIIPER research methodology with autonomous browsing
    """
    
    name: str = "Idea Generation Agent"
    role: AgentRole = AgentRole.RESEARCH
    capabilities: List[AgentCapability] = [
        AgentCapability.MARKET_RESEARCH,
        AgentCapability.COMPETITIVE_ANALYSIS,
        AgentCapability.DATA_ANALYSIS,
    ]
    
    # Trend sources
    TREND_SOURCES = {
        "product_hunt": "https://www.producthunt.com",
        "reddit_startup": "https://www.reddit.com/r/startups/hot",
        "reddit_saaS": "https://www.reddit.com/r/SaaS/hot",
        "indie_hackers": "https://www.indiehackers.com",
        "hacker_news": "https://news.ycombinator.com",
    }
    
    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Generate and score app ideas.
        
        Task metadata options:
        - niche: "productivity" | "AI" | "devtools" | etc.
        - category: IdeaCategory
        - min_score: minimum score threshold
        - max_ideas: maximum ideas to generate
        """
        niche = task.metadata.get("niche", "")
        category = task.metadata.get("category")
        min_score = task.metadata.get("min_score", 0.6)
        max_ideas = task.metadata.get("max_ideas", 10)
        
        # Step 1: Gather trend data
        trends = await self._gather_trends(niche)
        
        # Step 2: Analyze patterns
        patterns = await self._analyze_patterns(trends)
        
        # Step 3: Generate ideas
        raw_ideas = await self._generate_ideas(patterns, category)
        
        # Step 4: Score ideas
        scored_ideas = await self._score_ideas(raw_ideas)
        
        # Step 5: Filter and rank
        filtered_ideas = [
            idea for idea in scored_ideas
            if idea.score.overall >= min_score
        ]
        ranked_ideas = sorted(filtered_ideas, key=lambda x: x.score.overall, reverse=True)[:max_ideas]
        
        return {
            "task_id": task.id,
            "task_name": task.name,
            "niche": niche,
            "ideas": [idea.dict() for idea in ranked_ideas],
            "top_recommendation": ranked_ideas[0].dict() if ranked_ideas else None,
            "trends_analyzed": len(trends),
            "patterns_found": len(patterns),
            "confidence": 0.85,
        }
    
    async def _gather_trends(self, niche: str) -> List[Dict[str, Any]]:
        """Gather trending data from multiple sources."""
        trends = []
        
        # Use BrowserAgent to scrape sources
        browser = BrowserAgent()
        
        try:
            for source_name, source_url in self.TREND_SOURCES.items():
                try:
                    # Navigate to source
                    nav_task = AgentTask(
                        name=f"Browse {source_name}",
                        metadata={"type": "navigate", "url": source_url}
                    )
                    await browser.execute_task(nav_task)
                    
                    # Scrape content
                    scrape_task = AgentTask(
                        name=f"Scrape {source_name}",
                        metadata={
                            "type": "scrape",
                            "selector": "article, .post, .item",
                            "extract_links": True
                        }
                    )
                    result = await browser.execute_task(scrape_task)
                    
                    if result.get("success"):
                        trends.append({
                            "source": source_name,
                            "url": source_url,
                            "content": result["data"].get("content", ""),
                            "links": result["data"].get("links", []),
                        })
                        
                except Exception as e:
                    # Continue with other sources
                    continue
                    
        finally:
            await browser.teardown()
        
        return trends
    
    async def _analyze_patterns(self, trends: List[Dict]) -> List[Dict[str, Any]]:
        """Analyze trends to find patterns."""
        patterns = []
        
        # Extract common keywords
        all_text = " ".join([t["content"] for t in trends])
        keywords = self._extract_keywords(all_text)
        
        # Identify pain points
        pain_points = self._identify_pain_points(all_text)
        
        # Find market gaps
        gaps = self._find_market_gaps(trends)
        
        patterns = [
            {"type": "keywords", "data": keywords[:20]},
            {"type": "pain_points", "data": pain_points},
            {"type": "market_gaps", "data": gaps},
        ]
        
        return patterns
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract trending keywords from text."""
        # Simple keyword extraction (would use NLP in production)
        common_tech_words = [
            "AI", "automation", "workflow", "productivity", "API",
            "integration", "dashboard", "analytics", "collaboration",
            "real-time", "cloud", "mobile", "security", "privacy",
            "machine learning", "chatbot", "no-code", "low-code",
        ]
        
        found = []
        text_lower = text.lower()
        for word in common_tech_words:
            if word.lower() in text_lower:
                found.append(word)
        
        return list(set(found))
    
    def _identify_pain_points(self, text: str) -> List[str]:
        """Identify user pain points from text."""
        pain_patterns = [
            "wish there was",
            "hate having to",
            "annoying when",
            "why is it so hard",
            "takes too long",
            "should be easier",
            "need help with",
            "looking for alternative",
        ]
        
        pain_points = []
        sentences = text.split(".")
        
        for sentence in sentences:
            for pattern in pain_patterns:
                if pattern in sentence.lower():
                    pain_points.append(sentence.strip())
                    break
        
        return pain_points[:10]
    
    def _find_market_gaps(self, trends: List[Dict]) -> List[str]:
        """Identify market gaps from trend analysis."""
        # Look for underserved categories
        gaps = [
            "AI-powered personal productivity assistant",
            "Automated code review for small teams",
            "Privacy-first analytics for indie hackers",
            "No-code workflow automation for non-technical users",
        ]
        return gaps
    
    async def _generate_ideas(
        self,
        patterns: List[Dict],
        category: Optional[str]
    ) -> List[AppIdea]:
        """Generate idea candidates based on patterns."""
        ideas = []
        
        keywords = next((p["data"] for p in patterns if p["type"] == "keywords"), [])
        pain_points = next((p["data"] for p in patterns if p["type"] == "pain_points"), [])
        gaps = next((p["data"] for p in patterns if p["type"] == "market_gaps"), [])
        
        # Generate ideas from gaps
        for i, gap in enumerate(gaps):
            idea = AppIdea(
                id=f"idea_{i}",
                title=gap,
                description=f"A solution addressing: {gap}",
                category=IdeaCategory.SAAS if not category else IdeaCategory(category),
                problem=pain_points[0] if pain_points else "Unmet market need",
                solution=gap,
                target_audience="Small businesses and startups",
                key_features=["Core feature 1", "Core feature 2", "Core feature 3"],
                monetization=["Subscription", "Usage-based pricing"],
                competitors=["Competitor A", "Competitor B"],
                score=IdeaScore(),  # Will be filled by scoring
                trending_keywords=keywords[:5]
            )
            ideas.append(idea)
        
        return ideas
    
    async def _score_ideas(self, ideas: List[AppIdea]) -> List[AppIdea]:
        """Score ideas based on multiple factors."""
        for idea in ideas:
            # Calculate scores
            market_size = self._estimate_market_size(idea)
            competition = self._estimate_competition(idea)
            feasibility = self._estimate_feasibility(idea)
            time_to_mvp = self._estimate_time_to_mvp(idea)
            revenue_potential = self._estimate_revenue(idea)
            
            # Calculate overall score
            overall = (
                market_size * 0.25 +
                (1 - competition) * 0.20 +  # Lower competition is better
                feasibility * 0.20 +
                time_to_mvp * 0.15 +
                revenue_potential * 0.20
            )
            
            idea.score = IdeaScore(
                market_size=market_size,
                competition=competition,
                feasibility=feasibility,
                time_to_mvp=time_to_mvp,
                revenue_potential=revenue_potential,
                overall=overall
            )
        
        return ideas
    
    def _estimate_market_size(self, idea: AppIdea) -> float:
        """Estimate market size (0-1)."""
        # Simplified scoring based on category
        category_scores = {
            IdeaCategory.SAAS: 0.8,
            IdeaCategory.AI_PRODUCT: 0.9,
            IdeaCategory.PRODUCTIVITY: 0.85,
            IdeaCategory.DEV_TOOL: 0.7,
            IdeaCategory.FINTECH: 0.9,
        }
        return category_scores.get(idea.category, 0.5)
    
    def _estimate_competition(self, idea: AppIdea) -> float:
        """Estimate competition level (0-1, lower is better)."""
        # More competitors = higher score
        return min(len(idea.competitors) / 10, 1.0)
    
    def _estimate_feasibility(self, idea: AppIdea) -> float:
        """Estimate technical feasibility (0-1)."""
        # Simplified: assume all ideas are feasible for now
        return 0.7
    
    def _estimate_time_to_mvp(self, idea: AppIdea) -> float:
        """Estimate time to MVP (0-1, higher = faster)."""
        # Fewer features = faster MVP
        return max(0.5, 1 - len(idea.key_features) / 20)
    
    def _estimate_revenue(self, idea: AppIdea) -> float:
        """Estimate revenue potential (0-1)."""
        # Based on monetization strategy
        if len(idea.monetization) > 1:
            return 0.8
        return 0.6
```

---

### Sprint 2.2: Enhanced Orchestrator with Sub-Agent Spawning

#### 2.2.1 Créer l'orchestrateur amélioré

**Fichier**: `viiper/orchestrator/enhanced_orchestrator.py`

```python
"""
Enhanced Project Orchestrator with sub-agent spawning.

Combines patterns from:
- Claude Code: Single-threaded master loop
- Kimi K2.5: Dynamic sub-agent spawning, step limits
- Manus AI: Iterative agent loop
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import asyncio
from datetime import datetime

from viiper.core.project import Project
from viiper.core.phase import Phase
from viiper.core.iterative_loop import IterativeAgentLoop, LoopOutcome
from viiper.core.resource_manager import ResourceManager, SubAgentSpawner
from viiper.agents.base import Agent, AgentTask, AgentRole
from viiper.agents.factory import AgentFactory
from viiper.agents.browser import BrowserAgent
from viiper.agents.idea_generation import IdeaGenerationAgent


class PipelineStage(str, Enum):
    """Stages in the end-to-end pipeline."""
    DISCOVERY = "discovery"
    IDEATION = "ideation"
    VALIDATION = "validation"
    PRODUCTION = "production"
    DEPLOYMENT = "deployment"


class PipelineResult(BaseModel):
    """Result of pipeline execution."""
    stage: PipelineStage
    success: bool
    output: Dict[str, Any]
    sub_results: List[Dict[str, Any]] = Field(default_factory=list)
    steps_used: int = 0
    duration_seconds: float = 0.0


class FullPipelineResult(BaseModel):
    """Result of complete end-to-end execution."""
    user_request: str
    stages: List[PipelineResult]
    idea: Optional[Dict] = None
    code: Optional[Dict] = None
    deployed_url: Optional[str] = None
    total_duration: float
    success: bool


from enum import Enum


class EnhancedProjectOrchestrator:
    """
    Enhanced orchestrator with Browse → Idea → Code capability.
    
    Features:
    - Iterative agent loop
    - Sub-agent spawning with step limits
    - Parallel execution
    - Context sharing between stages
    
    Architecture inspired by:
    - Claude Code: Master loop pattern
    - Kimi K2.5: Sub-agent spawning (15/100 steps)
    - Manus AI: Analyze → Plan → Execute → Observe
    """
    
    def __init__(self, project: Optional[Project] = None):
        self.project = project
        self.resource_manager = ResourceManager("orchestrator")
        self.sub_agent_spawner = SubAgentSpawner(max_concurrent=10)
        self.iterative_loop = IterativeAgentLoop(max_iterations=50)
        self.context: Dict[str, Any] = {}
        
        # Agent pool
        self.agents: Dict[str, Agent] = {}
        self._initialize_agents()
    
    def _initialize_agents(self) -> None:
        """Initialize agent pool."""
        # Core agents
        self.agents["browser"] = BrowserAgent()
        self.agents["idea_gen"] = IdeaGenerationAgent()
        
        # Production agents from factory
        for agent_name in ["frontend", "backend", "testing", "devops"]:
            agent = AgentFactory.create_agent(agent_name)
            if agent:
                self.agents[agent_name] = agent
    
    async def execute_full_pipeline(
        self,
        user_request: str
    ) -> FullPipelineResult:
        """
        Execute complete Browse → Idea → Code pipeline.
        
        Args:
            user_request: User's request (e.g., "Find me a SaaS idea in productivity")
        
        Returns:
            FullPipelineResult with idea, code, and deployed URL
        """
        import time
        start_time = time.time()
        
        stages = []
        
        # Stage 1: Discovery
        discovery_result = await self._execute_discovery(user_request)
        stages.append(discovery_result)
        self.context["discovery"] = discovery_result.output
        
        # Stage 2: Ideation
        ideation_result = await self._execute_ideation(user_request)
        stages.append(ideation_result)
        self.context["idea"] = ideation_result.output.get("top_recommendation")
        
        # Stage 3: Validation
        if self.context.get("idea"):
            validation_result = await self._execute_validation(self.context["idea"])
            stages.append(validation_result)
        
        # Stage 4: Production
        if self.context.get("idea"):
            production_result = await self._execute_production(self.context["idea"])
            stages.append(production_result)
            self.context["code"] = production_result.output
        
        # Stage 5: Deployment
        if self.context.get("code"):
            deployment_result = await self._execute_deployment(self.context["code"])
            stages.append(deployment_result)
            self.context["deployed_url"] = deployment_result.output.get("url")
        
        total_duration = time.time() - start_time
        
        return FullPipelineResult(
            user_request=user_request,
            stages=stages,
            idea=self.context.get("idea"),
            code=self.context.get("code"),
            deployed_url=self.context.get("deployed_url"),
            total_duration=total_duration,
            success=stages[-1].success if stages else False
        )
    
    async def _execute_discovery(self, request: str) -> PipelineResult:
        """Execute discovery phase - browse for trends."""
        import time
        start = time.time()
        
        browser = self.agents["browser"]
        
        # Parse niche from request
        niche = self._extract_niche(request)
        
        # Search for trends
        search_task = AgentTask(
            name="Trend Search",
            description=f"Search for trends in {niche}",
            metadata={"type": "search", "query": f"{niche} startup ideas 2026"}
        )
        
        result = await browser.execute_task(search_task)
        
        return PipelineResult(
            stage=PipelineStage.DISCOVERY,
            success=result.get("success", False),
            output=result.get("data", {}),
            steps_used=1,
            duration_seconds=time.time() - start
        )
    
    async def _execute_ideation(self, request: str) -> PipelineResult:
        """Execute ideation phase - generate ideas."""
        import time
        start = time.time()
        
        idea_agent = self.agents["idea_gen"]
        
        niche = self._extract_niche(request)
        
        task = AgentTask(
            name="Generate Ideas",
            description=f"Generate app ideas in {niche}",
            metadata={"niche": niche, "max_ideas": 5}
        )
        
        result = await idea_agent.execute_task(task)
        
        return PipelineResult(
            stage=PipelineStage.IDEATION,
            success=result.get("success", True),
            output=result,
            steps_used=1,
            duration_seconds=time.time() - start
        )
    
    async def _execute_validation(self, idea: Dict) -> PipelineResult:
        """Execute validation phase."""
        import time
        start = time.time()
        
        # Use browser to validate idea
        browser = self.agents["browser"]
        
        # Check for existing competitors
        search_task = AgentTask(
            name="Competitor Search",
            description=f"Search for competitors to {idea.get('title', '')}",
            metadata={"type": "search", "query": f"{idea.get('title', '')} alternatives"}
        )
        
        result = await browser.execute_task(search_task)
        
        return PipelineResult(
            stage=PipelineStage.VALIDATION,
            success=True,
            output={"competitors": result.get("data", {}).get("results", [])},
            duration_seconds=time.time() - start
        )
    
    async def _execute_production(self, idea: Dict) -> PipelineResult:
        """Execute production phase - build MVP with sub-agents."""
        import time
        start = time.time()
        
        # Spawn parallel sub-agents for frontend and backend
        sub_results = []
        
        async def spawn_and_execute(agent_type: str, task_desc: str):
            agent = AgentFactory.create_agent(agent_type)
            if not agent:
                return {"error": f"Agent {agent_type} not found"}
            
            task = AgentTask(
                name=f"{agent_type} Development",
                description=task_desc,
                context={"idea": idea}
            )
            return await agent.execute_task(task)
        
        # Parallel execution
        results = await asyncio.gather(
            spawn_and_execute("frontend", "Build frontend for MVP"),
            spawn_and_execute("backend", "Build backend API for MVP"),
        )
        
        sub_results = list(results)
        
        return PipelineResult(
            stage=PipelineStage.PRODUCTION,
            success=True,
            output={
                "frontend": sub_results[0],
                "backend": sub_results[1]
            },
            sub_results=sub_results,
            duration_seconds=time.time() - start
        )
    
    async def _execute_deployment(self, code: Dict) -> PipelineResult:
        """Execute deployment phase."""
        import time
        start = time.time()
        
        devops = self.agents.get("devops")
        
        if not devops:
            return PipelineResult(
                stage=PipelineStage.DEPLOYMENT,
                success=False,
                output={"error": "DevOps agent not available"},
                duration_seconds=time.time() - start
            )
        
        task = AgentTask(
            name="Deploy MVP",
            description="Deploy the MVP to production",
            context={"code": code}
        )
        
        result = await devops.execute_task(task)
        
        return PipelineResult(
            stage=PipelineStage.DEPLOYMENT,
            success=result.get("success", False),
            output=result,
            duration_seconds=time.time() - start
        )
    
    def _extract_niche(self, request: str) -> str:
        """Extract niche/category from request."""
        niches = [
            "productivity", "AI", "devtools", "SaaS", "fintech",
            "health", "education", "ecommerce", "marketplace"
        ]
        
        request_lower = request.lower()
        for niche in niches:
            if niche.lower() in request_lower:
                return niche
        
        return "productivity"  # Default
    
    async def spawn_sub_agent(
        self,
        agent_type: str,
        task: AgentTask
    ) -> Dict[str, Any]:
        """Spawn a sub-agent with resource limits."""
        agent_id = f"{agent_type}_{datetime.now().timestamp()}"
        
        return await self.sub_agent_spawner.spawn(
            agent_id,
            lambda: AgentFactory.create_agent(agent_type),
            task
        )
    
    def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status."""
        return {
            "resource_manager": self.resource_manager.get_status(),
            "sub_agents_active": self.sub_agent_spawner.get_active_count(),
            "context_keys": list(self.context.keys()),
            "agents_available": list(self.agents.keys())
        }
```

---

## 🎯 Phase 3: Integration Layer (Semaines 5-6)

### Sprint 3.1: Context Sharing & Memory

#### 3.1.1 Système de contexte partagé

**Fichier**: `viiper/core/shared_context.py`

```python
"""
Shared context system for inter-agent communication.

Implements memory and context sharing between agents.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import json


class ContextEntry(BaseModel):
    """A single context entry."""
    key: str
    value: Any
    source_agent: str
    timestamp: datetime = Field(default_factory=datetime.now)
    tags: List[str] = Field(default_factory=list)


class SharedContext(BaseModel):
    """Shared context between agents."""
    project_id: str
    entries: Dict[str, ContextEntry] = Field(default_factory=dict)
    history: List[ContextEntry] = Field(default_factory=list)
    
    def set(self, key: str, value: Any, source_agent: str, tags: List[str] = None) -> None:
        """Set a context value."""
        entry = ContextEntry(
            key=key,
            value=value,
            source_agent=source_agent,
            tags=tags or []
        )
        self.entries[key] = entry
        self.history.append(entry)
    
    def get(self, key: str) -> Optional[Any]:
        """Get a context value."""
        entry = self.entries.get(key)
        return entry.value if entry else None
    
    def get_all_for_agent(self, agent_name: str) -> Dict[str, Any]:
        """Get all context entries relevant for an agent."""
        return {
            k: v.value
            for k, v in self.entries.items()
            if agent_name in v.tags or not v.tags
        }
    
    def get_history(self, limit: int = 100) -> List[Dict]:
        """Get context history."""
        return [
            {
                "key": e.key,
                "source": e.source_agent,
                "timestamp": e.timestamp.isoformat()
            }
            for e in self.history[-limit:]
        ]


class ContextManager:
    """Manages shared contexts for multiple projects."""
    
    def __init__(self):
        self.contexts: Dict[str, SharedContext] = {}
    
    def create_context(self, project_id: str) -> SharedContext:
        """Create a new shared context."""
        context = SharedContext(project_id=project_id)
        self.contexts[project_id] = context
        return context
    
    def get_context(self, project_id: str) -> Optional[SharedContext]:
        """Get existing context."""
        return self.contexts.get(project_id)
    
    def share_between_agents(
        self,
        project_id: str,
        from_agent: str,
        to_agent: str,
        key: str,
        value: Any
    ) -> None:
        """Share context between two agents."""
        context = self.get_context(project_id)
        if context:
            context.set(
                key=key,
                value=value,
                source_agent=from_agent,
                tags=[to_agent]
            )
```

---

### Sprint 3.2: Error Recovery System

#### 3.2.1 Système de récupération d'erreurs

**Fichier**: `viiper/core/error_recovery.py`

```python
"""
Error recovery system for robust agent execution.

Implements retry, fallback, and recovery mechanisms.
"""

from typing import Dict, Any, Optional, Callable, List
from pydantic import BaseModel, Field
from enum import Enum
import asyncio
from datetime import datetime


class ErrorType(str, Enum):
    """Types of errors."""
    NETWORK = "network"
    BROWSER = "browser"
    AGENT = "agent"
    RESOURCE = "resource"
    VALIDATION = "validation"
    UNKNOWN = "unknown"


class ErrorContext(BaseModel):
    """Context for an error."""
    error_type: ErrorType
    message: str
    agent_name: Optional[str] = None
    task_name: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    retry_count: int = 0
    recoverable: bool = True


class RecoveryStrategy(str, Enum):
    """Recovery strategies."""
    RETRY = "retry"
    FALLBACK = "fallback"
    SKIP = "skip"
    ABORT = "abort"


class RecoveryPlan(BaseModel):
    """Plan for recovering from an error."""
    error: ErrorContext
    strategy: RecoveryStrategy
    max_retries: int = 3
    retry_delay_seconds: float = 1.0
    fallback_agent: Optional[str] = None
    fallback_action: Optional[str] = None


class ErrorRecovery:
    """
    Handles error recovery for agent execution.
    
    Inspired by Manus AI's error handling patterns.
    """
    
    # Error type to recovery strategy mapping
    DEFAULT_STRATEGIES = {
        ErrorType.NETWORK: RecoveryStrategy.RETRY,
        ErrorType.BROWSER: RecoveryStrategy.RETRY,
        ErrorType.AGENT: RecoveryStrategy.FALLBACK,
        ErrorType.RESOURCE: RecoveryStrategy.SKIP,
        ErrorType.VALIDATION: RecoveryStrategy.ABORT,
        ErrorType.UNKNOWN: RecoveryStrategy.RETRY,
    }
    
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.error_history: List[ErrorContext] = []
    
    async def execute_with_recovery(
        self,
        task: Any,
        executor: Callable,
        fallback_executor: Optional[Callable] = None,
        on_error: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """Execute a task with automatic error recovery."""
        retry_count = 0
        
        while retry_count <= self.max_retries:
            try:
                result = await executor(task)
                return result
                
            except Exception as e:
                error = self._classify_error(e, task, retry_count)
                self.error_history.append(error)
                
                # Callback
                if on_error:
                    await on_error(error)
                
                # Get recovery strategy
                strategy = self._get_recovery_strategy(error)
                
                if strategy == RecoveryStrategy.RETRY and retry_count < self.max_retries:
                    retry_count += 1
                    await asyncio.sleep(self._get_backoff_delay(retry_count))
                    continue
                    
                elif strategy == RecoveryStrategy.FALLBACK and fallback_executor:
                    try:
                        return await fallback_executor(task)
                    except Exception as fallback_error:
                        return {
                            "success": False,
                            "error": str(fallback_error),
                            "recovery_attempted": True
                        }
                        
                elif strategy == RecoveryStrategy.SKIP:
                    return {
                        "success": False,
                        "skipped": True,
                        "reason": str(e)
                    }
                    
                else:
                    return {
                        "success": False,
                        "error": str(e),
                        "retries": retry_count
                    }
        
        return {
            "success": False,
            "error": "Max retries exceeded",
            "retries": retry_count
        }
    
    def _classify_error(
        self,
        exception: Exception,
        task: Any,
        retry_count: int
    ) -> ErrorContext:
        """Classify error type."""
        error_msg = str(exception).lower()
        
        if "network" in error_msg or "connection" in error_msg:
            error_type = ErrorType.NETWORK
        elif "browser" in error_msg or "page" in error_msg:
            error_type = ErrorType.BROWSER
        elif "agent" in error_msg:
            error_type = ErrorType.AGENT
        elif "resource" in error_msg or "limit" in error_msg:
            error_type = ErrorType.RESOURCE
        elif "validation" in error_msg:
            error_type = ErrorType.VALIDATION
        else:
            error_type = ErrorType.UNKNOWN
        
        return ErrorContext(
            error_type=error_type,
            message=str(exception),
            task_name=getattr(task, "name", None),
            retry_count=retry_count
        )
    
    def _get_recovery_strategy(self, error: ErrorContext) -> RecoveryStrategy:
        """Get recovery strategy for an error."""
        return self.DEFAULT_STRATEGIES.get(error.error_type, RecoveryStrategy.RETRY)
    
    def _get_backoff_delay(self, retry_count: int) -> float:
        """Calculate exponential backoff delay."""
        return min(2 ** retry_count, 30)  # Cap at 30 seconds
```

---

## 🎯 Phase 4: Polish & Demo (Semaine 7)

### Sprint 4.1: CLI Integration

#### 4.1.1 Commandes CLI pour le nouveau pipeline

**Fichier**: `viiper/cli/pipeline_commands.py`

```python
"""
CLI commands for the Browse → Idea → Code pipeline.
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import asyncio

from viiper.orchestrator.enhanced_orchestrator import EnhancedProjectOrchestrator

app = typer.Typer()
console = Console()


@app.command("browse-idea-code")
def browse_idea_code(
    request: str = typer.Argument(..., help="Your request, e.g., 'Find me a SaaS idea in productivity'"),
    deploy: bool = typer.Option(False, "--deploy", "-d", help="Deploy the MVP automatically"),
):
    """
    Execute the full Browse → Idea → Code pipeline.
    
    Example:
        viiper browse-idea-code "Find me a productivity SaaS idea"
    """
    console.print(f"[bold blue]Starting pipeline:[/] {request}")
    
    orchestrator = EnhancedProjectOrchestrator()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        async def run_pipeline():
            result = await orchestrator.execute_full_pipeline(request)
            return result
        
        # Run async pipeline
        result = asyncio.run(run_pipeline())
    
    # Display results
    _display_pipeline_result(result, deploy)


def _display_pipeline_result(result, deploy: bool):
    """Display pipeline results in a formatted way."""
    
    # Ideas table
    if result.idea:
        console.print("\n[bold green]💡 Top Idea:[/]")
        console.print(f"  Title: {result.idea.get('title', 'N/A')}")
        console.print(f"  Score: {result.idea.get('score', {}).get('overall', 0):.2f}")
        console.print(f"  Category: {result.idea.get('category', 'N/A')}")
    
    # Code status
    if result.code:
        console.print("\n[bold green]📝 Code Generated:[/]")
        console.print(f"  Frontend: {'✅' if result.code.get('frontend') else '❌'}")
        console.print(f"  Backend: {'✅' if result.code.get('backend') else '❌'}")
    
    # Deployment URL
    if result.deployed_url:
        console.print(f"\n[bold green]🚀 Deployed:[/] {result.deployed_url}")
    
    # Summary
    console.print(f"\n[bold]Summary:[/]")
    console.print(f"  Total duration: {result.total_duration:.1f}s")
    console.print(f"  Stages completed: {len(result.stages)}/5")
    console.print(f"  Success: {'✅' if result.success else '❌'}")


@app.command("browse")
def browse_only(
    query: str = typer.Argument(..., help="Search query"),
    source: str = typer.Option("all", "--source", "-s", help="Source to browse (producthunt, reddit, all)"),
):
    """
    Browse the web for trends and ideas.
    
    Example:
        viiper browse "AI productivity tools" --source producthunt
    """
    from viiper.agents.browser import BrowserAgent
    from viiper.agents.base import AgentTask
    
    console.print(f"[bold]Browsing for:[/] {query}")
    
    async def run_browse():
        agent = BrowserAgent()
        try:
            task = AgentTask(
                name="Browse",
                metadata={"type": "search", "query": query}
            )
            result = await agent.execute_task(task)
            return result
        finally:
            await agent.teardown()
    
    result = asyncio.run(run_browse())
    
    if result.get("success"):
        data = result.get("data", {})
        results = data.get("results", [])
        
        table = Table(title="Results")
        table.add_column("Title", style="cyan")
        table.add_column("URL", style="green")
        
        for r in results[:10]:
            table.add_row(
                r.get("title", "")[:50],
                r.get("url", "")[:50]
            )
        
        console.print(table)
    else:
        console.print(f"[red]Error: {result.get('error', 'Unknown error')}[/]")


@app.command("generate-ideas")
def generate_ideas(
    niche: str = typer.Argument(..., help="Niche/category"),
    count: int = typer.Option(5, "--count", "-c", help="Number of ideas to generate"),
):
    """
    Generate app ideas for a niche.
    
    Example:
        viiper generate-ideas productivity --count 10
    """
    from viiper.agents.idea_generation import IdeaGenerationAgent
    from viiper.agents.base import AgentTask
    
    console.print(f"[bold]Generating ideas for:[/] {niche}")
    
    async def run_generation():
        agent = IdeaGenerationAgent()
        task = AgentTask(
            name="Generate Ideas",
            metadata={"niche": niche, "max_ideas": count}
        )
        return await agent.execute_task(task)
    
    result = asyncio.run(run_generation())
    
    if result.get("ideas"):
        table = Table(title="Generated Ideas")
        table.add_column("#", style="dim")
        table.add_column("Title")
        table.add_column("Score")
        
        for i, idea in enumerate(result["ideas"], 1):
            table.add_row(
                str(i),
                idea.get("title", "")[:40],
                f"{idea.get('score', {}).get('overall', 0):.2f}"
            )
        
        console.print(table)


# Add to main CLI
# In viiper/cli/main.py, add:
# from viiper.cli.pipeline_commands import app as pipeline_app
# app.add_typer(pipeline_app, name="pipeline")
```

---

## 📊 Summary: Complete Implementation Checklist

### Phase 1: Foundation (Weeks 1-2)
- [ ] `viiper/agents/browser.py` - BrowserAgent with Playwright
- [ ] `viiper/core/iterative_loop.py` - IterativeAgentLoop
- [ ] `viiper/core/resource_manager.py` - Step limits & resource management
- [ ] `tests/unit/test_browser_agent.py` - Unit tests
- [ ] `tests/unit/test_iterative_loop.py` - Unit tests

### Phase 2: Intelligence (Weeks 3-4)
- [ ] `viiper/agents/idea_generation.py` - IdeaGenerationAgent
- [ ] `viiper/orchestrator/enhanced_orchestrator.py` - Enhanced orchestrator
- [ ] Sub-agent spawning integration
- [ ] Parallel execution support
- [ ] Integration tests

### Phase 3: Integration (Weeks 5-6)
- [ ] `viiper/core/shared_context.py` - Context sharing
- [ ] `viiper/core/error_recovery.py` - Error recovery
- [ ] End-to-end workflow tests
- [ ] Performance optimization

### Phase 4: Polish (Week 7)
- [ ] `viiper/cli/pipeline_commands.py` - CLI commands
- [ ] Documentation
- [ ] Demo project
- [ ] Quality gates

---

## 🎯 Success Metrics

| Metric | Target |
|--------|--------|
| Browse → Idea time | < 60 seconds |
| Idea generation | 5+ ideas per request |
| Code generation | Working MVP structure |
| End-to-end time | < 10 minutes |
| Test coverage | > 85% |
| Error recovery | > 90% success |

---

*Implementation Plan for VIIPER V4 - v0.2.0*
*Generated: 21/02/2026*