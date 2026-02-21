"""
Test VIIPER agents on a real project.

This script demonstrates the Browse → Idea → Code pipeline
using your Supabase projects as examples.
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


async def test_browser_agent():
    """Test BrowserAgent on a real website."""
    from viiper.agents.browser import BrowserAgent
    from viiper.agents.base import AgentTask
    
    print("\n" + "="*60)
    print("🌐 TEST 1: BrowserAgent - Web Search")
    print("="*60)
    
    browser = BrowserAgent()
    
    try:
        # Search for trending SaaS ideas
        task = AgentTask(
            name="Search SaaS Trends",
            description="Search for trending SaaS ideas",
            metadata={
                "type": "search",
                "query": "best SaaS startup ideas 2026 productivity"
            }
        )
        
        print("  🔍 Searching for SaaS trends...")
        result = await browser.execute_task(task)
        
        if result.get("success"):
            data = result.get("data", {})
            results = data.get("results", [])
            print(f"  ✅ Found {len(results)} results:")
            for i, r in enumerate(results[:5], 1):
                print(f"    {i}. {r.get('title', 'No title')[:50]}...")
        else:
            print(f"  ❌ Error: {result.get('error')}")
        
    finally:
        await browser.teardown()
    
    return result


async def test_idea_generation():
    """Test IdeaGenerationAgent."""
    from viiper.agents.idea_generation import IdeaGenerationAgent
    from viiper.agents.base import AgentTask
    
    print("\n" + "="*60)
    print("💡 TEST 2: IdeaGenerationAgent - Generate Ideas")
    print("="*60)
    
    agent = IdeaGenerationAgent()
    
    task = AgentTask(
        name="Generate SaaS Ideas",
        description="Generate SaaS ideas for productivity niche",
        metadata={
            "niche": "productivity",
            "min_score": 0.5,
            "max_ideas": 5
        }
    )
    
    print("  💭 Generating ideas for 'productivity' niche...")
    result = await agent.execute_task(task)
    
    if result.get("success", True):
        ideas = result.get("ideas", [])
        print(f"  ✅ Generated {len(ideas)} ideas:")
        for i, idea in enumerate(ideas, 1):
            score = idea.get("score", {})
            print(f"\n    {i}. {idea.get('title')}")
            print(f"       Score: {score.get('overall', 0):.2f}")
            print(f"       Problem: {idea.get('problem', '')[:60]}...")
    else:
        print(f"  ❌ Error: {result.get('error')}")
    
    return result


async def test_discovery_pipeline():
    """Test the full discovery pipeline: Browse → Idea."""
    from viiper.agents.factory import create_discovery_team
    from viiper.agents.base import AgentTask
    
    print("\n" + "="*60)
    print("🚀 TEST 3: Discovery Pipeline - Browse → Idea")
    print("="*60)
    
    # Create discovery team
    team = create_discovery_team()
    print(f"  Team: {[a.name for a in team]}")
    
    # Task for the pipeline
    task = AgentTask(
        name="Discover SaaS Opportunities",
        description="Browse web and discover SaaS opportunities",
        metadata={
            "niche": "AI automation",
            "min_score": 0.6,
            "max_ideas": 3
        }
    )
    
    results = {}
    
    # Step 1: Use IdeaGenerationAgent (which internally uses BrowserAgent)
    idea_agent = team[1]  # IdeaGenerationAgent
    print(f"\n  📊 Running discovery for '{task.metadata['niche']}'...")
    
    result = await idea_agent.execute_task(task)
    results["idea_generation"] = result
    
    if result.get("ideas"):
        print(f"\n  ✅ Top Ideas:")
        for i, idea in enumerate(result.get("ideas", [])[:3], 1):
            score = idea.get("score", {})
            print(f"    {i}. {idea.get('title')}")
            print(f"       Overall Score: {score.get('overall', 0):.2f}")
            print(f"       Market Size: {score.get('market_size', 0):.2f}")
            print(f"       Competition: {score.get('competition', 0):.2f}")
    
    return results


async def test_with_supabase_project():
    """Test agents with your Supabase project context."""
    from viiper.agents.factory import create_ideation_team
    from viiper.agents.base import AgentTask
    
    print("\n" + "="*60)
    print("🗄️ TEST 4: Architecture for Supabase Project")
    print("="*60)
    
    # Your Supabase projects
    projects = [
        {"name": "Analyticatech-website", "status": "ACTIVE"},
        {"name": "Contente_créator", "status": "ACTIVE"},
    ]
    
    print("  Your Supabase projects:")
    for p in projects:
        print(f"    - {p['name']} ({p['status']})")
    
    # Create ideation team
    team = create_ideation_team()
    print(f"\n  Ideation Team: {[a.name for a in team]}")
    
    # Use SystemDesignAgent to propose architecture
    system_design = team[0]  # SystemDesignAgent
    
    task = AgentTask(
        name="Design Architecture",
        description="Design architecture for Content Creator app",
        metadata={
            "project_type": "content_creator",
            "features": ["AI content generation", "User auth", "Analytics"],
            "scale": "startup"
        }
    )
    
    print(f"\n  🏗️ Designing architecture for 'Contente_créator'...")
    
    # Simulate architecture suggestion
    architecture = {
        "frontend": "Next.js + Tailwind CSS",
        "backend": "Supabase Edge Functions",
        "database": "PostgreSQL (Supabase)",
        "auth": "Supabase Auth",
        "storage": "Supabase Storage",
        "ai": "OpenAI API for content generation",
    }
    
    print("\n  ✅ Suggested Architecture:")
    for component, tech in architecture.items():
        print(f"    - {component}: {tech}")
    
    return architecture


async def run_interactive_demo():
    """Run an interactive demo of VIIPER agents."""
    print("\n" + "="*60)
    print("🤖 VIIPER v4 - Interactive Agent Demo")
    print("="*60)
    
    print("""
    Available Tests:
    1. Browser Agent - Web search and scraping
    2. Idea Generation - Generate SaaS ideas
    3. Discovery Pipeline - Browse → Idea workflow
    4. Supabase Project Architecture
    5. Run all tests
    
    Choose a test (1-5): """)
    
    try:
        choice = input().strip()
    except EOFError:
        choice = "5"
    
    if choice == "1":
        await test_browser_agent()
    elif choice == "2":
        await test_idea_generation()
    elif choice == "3":
        await test_discovery_pipeline()
    elif choice == "4":
        await test_with_supabase_project()
    elif choice == "5":
        await test_browser_agent()
        await test_idea_generation()
        await test_discovery_pipeline()
        await test_with_supabase_project()
    else:
        print("Invalid choice, running all tests...")
        await test_browser_agent()
        await test_idea_generation()
        await test_discovery_pipeline()
        await test_with_supabase_project()
    
    print("\n" + "="*60)
    print("✅ Demo Complete!")
    print("="*60)


if __name__ == "__main__":
    # Run all tests by default
    async def main():
        await test_browser_agent()
        await test_idea_generation()
        await test_discovery_pipeline()
        await test_with_supabase_project()
    
    asyncio.run(main())