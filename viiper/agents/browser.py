"""
Browser Agent for autonomous web navigation.

Enables VIIPER to browse the web, scrape content, and interact with pages.
This agent is critical for the Browse → Idea → Code pipeline.

SECURITY: All inputs are sanitized to prevent prompt injection and XSS.
"""

from typing import Dict, Any, List, Optional
from viiper.agents.base import Agent, AgentRole, AgentCapability, AgentTask
from viiper.security import (
    PromptInjectionGuard,
    sanitize_url,
    validate_search_query,
    ContentFilter,
    filter_sensitive_data,
)
from pydantic import Field
from datetime import datetime
from enum import Enum
import base64
import logging

logger = logging.getLogger(__name__)


class BrowserCapability(str, Enum):
    """Capabilities for browser operations."""
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
    
    SECURITY FEATURES:
    - All URLs sanitized before navigation
    - Search queries validated against injection
    - Scraped content filtered for malicious patterns
    - Input validation on all operations
    
    Inspired by: Manus AI browser integration
    """
    
    name: str = "Browser Agent"
    role: AgentRole = AgentRole.SPECIALIST
    # Use string capabilities for browser-specific operations
    capabilities: List[Any] = Field(default_factory=lambda: [])
    browser_capabilities: List[BrowserCapability] = Field(default_factory=lambda: [
        BrowserCapability.WEB_NAVIGATION,
        BrowserCapability.CONTENT_SCRAPING,
        BrowserCapability.SCREENSHOT_CAPTURE,
        BrowserCapability.FORM_INTERACTION,
        BrowserCapability.SEARCH,
    ])
    skills: List[str] = Field(default_factory=lambda: [
        "playwright",
        "web_scraping",
        "screenshot_capture",
        "form_automation",
        "search_queries",
    ])
    
    # Browser state (internal) - using private attributes
    _playwright: Any = None
    _browser: Any = None
    _page: Any = None
    session_history: List[Dict] = Field(default_factory=list)
    
    # Security
    _security_guard: Any = None
    _content_filter: Any = None
    
    model_config = {"arbitrary_types_allowed": True}
    
    def __init__(self, **data):
        super().__init__(**data)
        # Initialize security components
        self._security_guard = PromptInjectionGuard(strict_mode=True)
        self._content_filter = ContentFilter(filter_pii=False, strict_mode=True)
    
    async def setup(self) -> None:
        """Initialize browser session."""
        if self._browser is None:
            try:
                from playwright.async_api import async_playwright
                self._playwright = await async_playwright().start()
                self._browser = await self._playwright.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )
                self._page = await self._browser.new_page()
            except ImportError:
                raise ImportError(
                    "Playwright not installed. Run: pip install playwright && playwright install"
                )
    
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
        
        Task types (via metadata["type"]):
        - navigate: Go to URL
        - scrape: Extract content
        - screenshot: Capture page
        - search: Web search
        - interact: Click, type, fill
        - extract: Structured extraction
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
            elif task_type == "click":
                result = await self._click(task.metadata.get("selector"))
            elif task_type == "type":
                result = await self._type_text(
                    task.metadata.get("selector"),
                    task.metadata.get("text", "")
                )
            else:
                result = {"error": f"Unknown task type: {task_type}"}
            
            # Log to session history
            self.session_history.append({
                "timestamp": datetime.now().isoformat(),
                "task_type": task_type,
                "result_summary": {k: v for k, v in result.items() if k not in ["raw_content", "screenshot"]}
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
        """Navigate to URL with security validation."""
        if not url:
            return {"error": "URL is required"}
        
        # SECURITY: Validate URL
        try:
            url = sanitize_url(url, strict=True)
        except ValueError as e:
            logger.warning(f"Blocked unsafe URL: {url}")
            return {"error": f"Unsafe URL blocked: {str(e)}"}
        
        await self._page.goto(url, wait_until="networkidle", timeout=30000)
        
        return {
            "url": self._page.url,
            "title": await self._page.title(),
            "status": "success"
        }
    
    async def _scrape(self, metadata: Dict) -> Dict[str, Any]:
        """Scrape content from page with security filtering."""
        selector = metadata.get("selector", "body")
        extract_links = metadata.get("extract_links", False)
        extract_images = metadata.get("extract_images", False)
        
        # Get text content
        elements = await self._page.query_selector_all(selector)
        texts = []
        for el in elements:
            text = await el.text_content()
            if text:
                texts.append(text.strip())
        
        raw_content = "\n".join(texts)
        
        # SECURITY: Filter scraped content
        filter_result = self._content_filter.filter(raw_content, "html")
        if not filter_result.is_safe:
            logger.warning(f"Blocked malicious content from {self._page.url}")
            raw_content = filter_result.filtered_content
        
        result = {
            "content": raw_content,
            "url": self._page.url,
            "element_count": len(elements),
            "security_warnings": filter_result.warnings if filter_result.warnings else None,
        }
        
        if extract_links:
            links = await self._page.query_selector_all("a[href]")
            result["links"] = []
            for link in links[:50]:
                text = await link.text_content()
                href = await link.get_attribute("href")
                if href:
                    result["links"].append({
                        "text": text.strip() if text else "",
                        "href": href
                    })
        
        if extract_images:
            images = await self._page.query_selector_all("img[src]")
            result["images"] = []
            for img in images[:20]:
                alt = await img.get_attribute("alt")
                src = await img.get_attribute("src")
                if src:
                    result["images"].append({
                        "alt": alt or "",
                        "src": src
                    })
        
        return result
    
    async def _screenshot(self, full_page: bool = True) -> Dict[str, Any]:
        """Capture screenshot."""
        screenshot_bytes = await self._page.screenshot(full_page=full_page)
        screenshot_base64 = base64.b64encode(screenshot_bytes).decode()
        
        return {
            "screenshot": screenshot_base64,
            "url": self._page.url,
            "full_page": full_page,
            "size_bytes": len(screenshot_bytes)
        }
    
    async def _search(self, query: str) -> Dict[str, Any]:
        """Perform web search using DuckDuckGo with security validation."""
        from urllib.parse import quote
        
        # SECURITY: Validate search query
        try:
            query = validate_search_query(query, max_length=500)
        except ValueError as e:
            logger.warning(f"Blocked unsafe search query: {query}")
            return {"error": f"Invalid search query: {str(e)}", "results": []}
        
        search_url = f"https://duckduckgo.com/?q={quote(query)}"
        await self._page.goto(search_url, wait_until="networkidle", timeout=30000)
        
        # Wait for results to load
        try:
            await self._page.wait_for_selector('[data-testid="result"]', timeout=10000)
        except:
            try:
                await self._page.wait_for_selector('.result', timeout=5000)
            except:
                pass
        
        # Extract results
        results = await self._page.query_selector_all('[data-testid="result"], .result')
        
        search_results = []
        for result in results[:10]:
            try:
                title_el = await result.query_selector("h2, .result__title")
                link_el = await result.query_selector("a[href]")
                snippet_el = await result.query_selector('[data-testid="result-snippet"], .result__snippet')
                
                if title_el and link_el:
                    title = await title_el.text_content()
                    href = await link_el.get_attribute("href")
                    snippet = await snippet_el.text_content() if snippet_el else ""
                    
                    search_results.append({
                        "title": title.strip() if title else "",
                        "url": href or "",
                        "snippet": snippet.strip() if snippet else ""
                    })
            except:
                continue
        
        return {
            "query": query,
            "results": search_results,
            "count": len(search_results),
            "source": "DuckDuckGo"
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
        elif action == "hover":
            await self._page.hover(selector)
        elif action == "scroll":
            await self._page.evaluate(f"window.scrollBy(0, {metadata.get('amount', 500)})")
        
        return {
            "action": action,
            "selector": selector,
            "status": "success",
            "url": self._page.url
        }
    
    async def _click(self, selector: str) -> Dict[str, Any]:
        """Click an element."""
        await self._page.click(selector)
        return {
            "action": "click",
            "selector": selector,
            "status": "success",
            "url": self._page.url
        }
    
    async def _type_text(self, selector: str, text: str) -> Dict[str, Any]:
        """Type text into an element."""
        await self._page.fill(selector, text)
        return {
            "action": "type",
            "selector": selector,
            "text": text,
            "status": "success"
        }
    
    async def _extract_structured(self, metadata: Dict) -> Dict[str, Any]:
        """Extract structured data using selectors."""
        schema = metadata.get("schema", {})
        results = {}
        
        for field_name, selector in schema.items():
            elements = await self._page.query_selector_all(selector)
            values = []
            for el in elements:
                text = await el.text_content()
                if text:
                    values.append(text.strip())
            results[field_name] = values
        
        return {
            "extracted": results,
            "url": self._page.url
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get browser agent statistics."""
        base_stats = super().get_stats()
        base_stats["browser"] = {
            "session_active": self._browser is not None,
            "pages_visited": len(self.session_history),
            "last_visit": self.session_history[-1] if self.session_history else None
        }
        return base_stats
    
    def get_session_history(self) -> List[Dict]:
        """Get the session history."""
        return self.session_history.copy()
    
    def clear_history(self) -> None:
        """Clear the session history."""
        self.session_history = []
