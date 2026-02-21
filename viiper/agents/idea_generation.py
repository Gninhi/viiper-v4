"""
Idea Generation Agent for autonomous idea discovery.

Analyzes trends, identifies opportunities, and generates app ideas.
"""

from typing import Dict, Any, List, Optional, ClassVar
from viiper.agents.base import Agent, AgentRole, AgentCapability, AgentTask
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
    market_size: float = Field(ge=0, le=1, default=0.5)
    competition: float = Field(ge=0, le=1, default=0.5)
    feasibility: float = Field(ge=0, le=1, default=0.5)
    time_to_mvp: float = Field(ge=0, le=1, default=0.5)
    revenue_potential: float = Field(ge=0, le=1, default=0.5)
    overall: float = Field(ge=0, le=1, default=0.5)


class AppIdea(BaseModel):
    """A generated app idea."""
    id: str
    title: str
    description: str
    category: IdeaCategory = IdeaCategory.SAAS
    problem: str = ""
    solution: str = ""
    target_audience: str = ""
    key_features: List[str] = Field(default_factory=list)
    monetization: List[str] = Field(default_factory=list)
    competitors: List[str] = Field(default_factory=list)
    score: IdeaScore = Field(default_factory=IdeaScore)
    trending_keywords: List[str] = Field(default_factory=list)


class IdeaGenerationAgent(Agent):
    """
    Agent specialized in generating and validating app ideas.
    
    Workflow:
    1. Browse trending sources (Product Hunt, Twitter, Reddit)
    2. Analyze market patterns
    3. Identify gaps and opportunities
    4. Generate idea candidates
    5. Score and rank ideas
    """
    
    name: str = "Idea Generation Agent"
    role: AgentRole = AgentRole.RESEARCH
    capabilities: List[AgentCapability] = Field(default_factory=lambda: [
        AgentCapability.MARKET_RESEARCH,
        AgentCapability.COMPETITIVE_ANALYSIS,
        AgentCapability.DATA_ANALYSIS,
    ])
    skills: List[str] = Field(default_factory=lambda: [
        "market_analysis",
        "trend_detection",
        "idea_scoring",
        "competitive_research",
    ])
    
    # Trend sources (ClassVar to avoid Pydantic field annotation issue)
    TREND_SOURCES: ClassVar[Dict[str, str]] = {
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
        - min_score: minimum score threshold (default: 0.6)
        - max_ideas: maximum ideas to generate (default: 10)
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
        raw_ideas = await self._generate_ideas(patterns, category, niche)
        
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
            "ideas": [idea.model_dump() for idea in ranked_ideas],
            "top_recommendation": ranked_ideas[0].model_dump() if ranked_ideas else None,
            "trends_analyzed": len(trends),
            "patterns_found": len(patterns),
            "confidence": 0.85,
        }
    
    async def _gather_trends(self, niche: str) -> List[Dict[str, Any]]:
        """Gather trending data from multiple sources."""
        trends = []
        
        # Try to use BrowserAgent if available
        try:
            from viiper.agents.browser import BrowserAgent
            browser = BrowserAgent()
            
            try:
                # Search for trends
                search_query = f"{niche} startup ideas trends 2026" if niche else "startup ideas trends 2026"
                
                search_task = AgentTask(
                    name="Trend Search",
                    description="Search for trending startup ideas",
                    metadata={"type": "search", "query": search_query}
                )
                result = await browser.execute_task(search_task)
                
                if result.get("success"):
                    data = result.get("data", {})
                    trends.append({
                        "source": "web_search",
                        "query": search_query,
                        "results": data.get("results", []),
                    })
                
                # Also browse specific sources
                for source_name, source_url in list(self.TREND_SOURCES.items())[:2]:
                    try:
                        nav_task = AgentTask(
                            name=f"Browse {source_name}",
                            metadata={"type": "navigate", "url": source_url}
                        )
                        nav_result = await browser.execute_task(nav_task)
                        
                        if nav_result.get("success"):
                            scrape_task = AgentTask(
                                name=f"Scrape {source_name}",
                                metadata={"type": "scrape", "selector": "article, .post, .item, .story"}
                            )
                            scrape_result = await browser.execute_task(scrape_task)
                            
                            if scrape_result.get("success"):
                                trends.append({
                                    "source": source_name,
                                    "url": source_url,
                                    "content": scrape_result.get("data", {}).get("content", ""),
                                })
                    except:
                        continue
                        
            finally:
                await browser.teardown()
                
        except ImportError:
            # BrowserAgent not available, use fallback
            trends = self._get_fallback_trends(niche)
        
        return trends
    
    def _get_fallback_trends(self, niche: str) -> List[Dict[str, Any]]:
        """Fallback trends when browser is not available."""
        return [
            {
                "source": "fallback",
                "content": f"Trending in {niche}: AI automation, productivity tools, no-code platforms",
            }
        ]
    
    async def _analyze_patterns(self, trends: List[Dict]) -> List[Dict[str, Any]]:
        """Analyze trends to find patterns."""
        patterns = []
        
        # Extract keywords from all content
        all_text = " ".join([
            t.get("content", "") + " " + str(t.get("results", ""))
            for t in trends
        ])
        
        keywords = self._extract_keywords(all_text)
        pain_points = self._identify_pain_points(all_text)
        gaps = self._find_market_gaps(trends)
        
        patterns = [
            {"type": "keywords", "data": keywords[:20]},
            {"type": "pain_points", "data": pain_points},
            {"type": "market_gaps", "data": gaps},
        ]
        
        return patterns
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract trending keywords from text."""
        common_tech_words = [
            "AI", "automation", "workflow", "productivity", "API",
            "integration", "dashboard", "analytics", "collaboration",
            "real-time", "cloud", "mobile", "security", "privacy",
            "machine learning", "chatbot", "no-code", "low-code",
            "SaaS", "B2B", "enterprise", "startup", "MVP",
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
        gaps = [
            "AI-powered personal productivity assistant",
            "Automated code review for small teams",
            "Privacy-first analytics for indie hackers",
            "No-code workflow automation for non-technical users",
            "Smart email management with AI",
            "Automated social media content generation",
            "Real-time collaboration for remote teams",
            "AI-powered customer support automation",
        ]
        return gaps
    
    async def _generate_ideas(
        self,
        patterns: List[Dict],
        category: Optional[str],
        niche: str
    ) -> List[AppIdea]:
        """Generate idea candidates based on patterns."""
        ideas = []
        
        keywords = next((p["data"] for p in patterns if p["type"] == "keywords"), [])
        pain_points = next((p["data"] for p in patterns if p["type"] == "pain_points"), [])
        gaps = next((p["data"] for p in patterns if p["type"] == "market_gaps"), [])
        
        # Generate ideas from gaps
        for i, gap in enumerate(gaps[:5]):
            idea = AppIdea(
                id=f"idea_{i}_{hash(gap) % 10000}",
                title=gap,
                description=f"A solution addressing: {gap}",
                category=IdeaCategory(category) if category else IdeaCategory.SAAS,
                problem=pain_points[0] if pain_points else "Unmet market need",
                solution=gap,
                target_audience="Small businesses and startups",
                key_features=[
                    "Core feature 1",
                    "Core feature 2",
                    "Core feature 3"
                ],
                monetization=["Subscription", "Usage-based pricing"],
                competitors=["Competitor A", "Competitor B"],
                score=IdeaScore(),
                trending_keywords=keywords[:5]
            )
            ideas.append(idea)
        
        # Add niche-specific idea if provided
        if niche:
            ideas.append(AppIdea(
                id=f"idea_niche_{hash(niche) % 10000}",
                title=f"{niche.capitalize()} automation platform",
                description=f"All-in-one platform for {niche} professionals",
                category=IdeaCategory(category) if category else IdeaCategory.SAAS,
                problem=f"Professionals in {niche} lack unified tools",
                solution=f"Integrated platform for {niche} workflows",
                target_audience=f"{niche.capitalize()} professionals",
                key_features=["Dashboard", "Analytics", "Automation"],
                monetization=["Freemium", "Pro subscription"],
                competitors=["Generic tool A"],
                trending_keywords=keywords[:3]
            ))
        
        return ideas
    
    async def _score_ideas(self, ideas: List[AppIdea]) -> List[AppIdea]:
        """Score ideas based on multiple factors."""
        for idea in ideas:
            market_size = self._estimate_market_size(idea)
            competition = self._estimate_competition(idea)
            feasibility = self._estimate_feasibility(idea)
            time_to_mvp = self._estimate_time_to_mvp(idea)
            revenue_potential = self._estimate_revenue(idea)
            
            overall = (
                market_size * 0.25 +
                (1 - competition) * 0.20 +
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
        category_scores = {
            IdeaCategory.SAAS: 0.8,
            IdeaCategory.AI_PRODUCT: 0.9,
            IdeaCategory.PRODUCTIVITY: 0.85,
            IdeaCategory.DEV_TOOL: 0.7,
            IdeaCategory.FINTECH: 0.9,
            IdeaCategory.HEALTH: 0.85,
            IdeaCategory.EDUCATION: 0.75,
        }
        return category_scores.get(idea.category, 0.5)
    
    def _estimate_competition(self, idea: AppIdea) -> float:
        """Estimate competition level (0-1, lower is better)."""
        return min(len(idea.competitors) / 10, 0.8)
    
    def _estimate_feasibility(self, idea: AppIdea) -> float:
        """Estimate technical feasibility (0-1)."""
        return 0.7
    
    def _estimate_time_to_mvp(self, idea: AppIdea) -> float:
        """Estimate time to MVP (0-1, higher = faster)."""
        return max(0.5, 1 - len(idea.key_features) / 20)
    
    def _estimate_revenue(self, idea: AppIdea) -> float:
        """Estimate revenue potential (0-1)."""
        if len(idea.monetization) > 1:
            return 0.8
        return 0.6