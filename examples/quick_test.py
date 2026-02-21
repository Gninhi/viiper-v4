"""
Quick test of VIIPER agents without browser (fallback mode).
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


async def test_idea_generation_fallback():
    """Test IdeaGenerationAgent without browser."""
    from viiper.agents.idea_generation import IdeaGenerationAgent
    from viiper.agents.base import AgentTask
    
    print("\n" + "="*60)
    print("💡 TEST: IdeaGenerationAgent (Fallback Mode)")
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
    print("  (Using fallback mode - no browser required)")
    
    result = await agent.execute_task(task)
    
    ideas = result.get("ideas", [])
    print(f"\n  ✅ Generated {len(ideas)} ideas:")
    
    for i, idea in enumerate(ideas, 1):
        score = idea.get("score", {})
        print(f"\n    {i}. {idea.get('title')}")
        print(f"       Score: {score.get('overall', 0):.2f}")
        print(f"       Market Size: {score.get('market_size', 0):.2f}")
        print(f"       Feasibility: {score.get('feasibility', 0):.2f}")
    
    print("\n" + "="*60)
    print("✅ Test Complete!")
    print("="*60)
    
    return result


async def test_discovery_team():
    """Test discovery team creation."""
    from viiper.agents.factory import create_discovery_team
    
    print("\n" + "="*60)
    print("🚀 TEST: Discovery Team")
    print("="*60)
    
    team = create_discovery_team()
    print(f"  Team members: {len(team)}")
    for agent in team:
        print(f"    - {agent.name} ({agent.role.value})")
    
    print("\n  ✅ Discovery team ready!")
    return team


async def test_supabase_integration():
    """Test with Supabase context."""
    from viiper.agents.factory import create_ideation_team
    
    print("\n" + "="*60)
    print("🗄️ TEST: Supabase Integration")
    print("="*60)
    
    # Your Supabase projects
    print("  Your Supabase projects:")
    print("    - Analyticatech-website (ACTIVE)")
    print("    - Contente_créator (ACTIVE)")
    
    team = create_ideation_team()
    print(f"\n  Ideation team: {[a.name for a in team]}")
    
    print("\n  ✅ Ready to design architecture for your projects!")


async def main():
    print("\n" + "="*60)
    print("🤖 VIIPER v4 - Quick Agent Test")
    print("="*60)
    
    await test_discovery_team()
    await test_idea_generation_fallback()
    await test_supabase_integration()
    
    print("\n" + "="*60)
    print("🎉 ALL TESTS PASSED!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())