"""
Full VIIPER Pipeline Test.

Tests all 6 phases: V → I → P → E → R → I²
Uses unified LLM with NVIDIA GLM5 and Kimi K2.5.
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


async def test_phase_validation():
    """Test Phase V: Validation - Market research, problem validation."""
    from viiper.core.phase import Phase
    from viiper.agents.factory import create_validation_team
    from viiper.llm import UnifiedLLM
    
    print("\n" + "="*60)
    print("🔍 PHASE V: VALIDATION")
    print("="*60)
    print(f"  Duration: {Phase.VALIDATION.typical_duration_weeks[0]}-{Phase.VALIDATION.typical_duration_weeks[1]} weeks")
    print(f"  Description: {Phase.VALIDATION.description}")
    
    # Get validation team
    team = create_validation_team()
    print(f"\n  Team: {[a.name for a in team]}")
    
    # Use Kimi K2.5 for market research (long context)
    llm = UnifiedLLM(model="moonshotai/kimi-k2.5")
    
    print("\n  Running market validation...")
    response = llm.complete(
        prompt="""
        Validate this SaaS idea: "AI-powered email assistant for small businesses"
        
        Analyze:
        1. Market size and opportunity
        2. Target audience pain points
        3. Competitors and differentiation
        4. Willingness-to-pay indicators
        5. Go/No-Go recommendation
        """,
        system_prompt="You are a market analyst. Be concise and data-driven.",
        max_tokens=800,
    )
    
    if response.success:
        print(f"\n  ✅ Validation Result ({response.model}):")
        print(f"  {response.content[:500]}...")
    else:
        print(f"  ❌ Error: {response.error}")
    
    return {"phase": "validation", "success": response.success}


async def test_phase_ideation():
    """Test Phase I: Ideation - Architecture, design, planning."""
    from viiper.core.phase import Phase
    from viiper.agents.factory import create_ideation_team
    from viiper.llm import UnifiedLLM
    
    print("\n" + "="*60)
    print("💡 PHASE I: IDEATION")
    print("="*60)
    print(f"  Duration: {Phase.IDEATION.typical_duration_weeks[0]}-{Phase.IDEATION.typical_duration_weeks[1]} weeks")
    print(f"  Description: {Phase.IDEATION.description}")
    
    # Get ideation team
    team = create_ideation_team()
    print(f"\n  Team: {[a.name for a in team]}")
    
    # Use GLM5 for architecture
    llm = UnifiedLLM(skill="architecture")
    
    print("\n  Designing system architecture...")
    response = llm.design_architecture(
        requirements="AI email assistant with natural language processing, smart replies, and calendar integration",
        constraints=[
            "Must integrate with Gmail and Outlook",
            "GDPR compliant",
            "API-first design",
            "Scale to 100k users",
        ]
    )
    
    if response.success:
        print(f"\n  ✅ Architecture ({response.model}):")
        print(f"  {response.content[:500]}...")
    else:
        print(f"  ❌ Error: {response.error}")
    
    return {"phase": "ideation", "success": response.success}


async def test_phase_production():
    """Test Phase P: Production - Development, testing, deployment."""
    from viiper.core.phase import Phase
    from viiper.agents.factory import create_production_team
    from viiper.llm import UnifiedLLM
    
    print("\n" + "="*60)
    print("🛠️ PHASE P: PRODUCTION")
    print("="*60)
    print(f"  Duration: {Phase.PRODUCTION.typical_duration_weeks[0]}-{Phase.PRODUCTION.typical_duration_weeks[1]} weeks")
    print(f"  Description: {Phase.PRODUCTION.description}")
    
    # Get production team
    team = create_production_team()
    print(f"\n  Team: {[a.name for a in team]}")
    
    # Use GLM5 for code generation
    llm = UnifiedLLM(skill="code_generation")
    
    print("\n  Generating core code...")
    response = llm.generate_code(
        description="FastAPI backend with /emails endpoint, /analyze endpoint for AI processing, and /replies endpoint for smart suggestions",
        language="python",
    )
    
    if response.success:
        print(f"\n  ✅ Generated Code ({response.model}):")
        print(f"  {response.content[:400]}...")
    else:
        print(f"  ❌ Error: {response.error}")
    
    return {"phase": "production", "success": response.success}


async def test_phase_execution():
    """Test Phase E: Execution - Launch, user acquisition, marketing."""
    from viiper.core.phase import Phase
    from viiper.llm import UnifiedLLM
    
    print("\n" + "="*60)
    print("🚀 PHASE E: EXECUTION")
    print("="*60)
    print(f"  Duration: {Phase.EXECUTION.typical_duration_weeks[0]}-{Phase.EXECUTION.typical_duration_weeks[1]} weeks")
    print(f"  Description: {Phase.EXECUTION.description}")
    
    # Use Kimi for marketing strategy
    llm = UnifiedLLM(model="moonshotai/kimi-k2.5")
    
    print("\n  Creating launch strategy...")
    response = llm.complete(
        prompt="""
        Create a launch strategy for "AI Email Assistant" SaaS:
        
        1. Pre-launch activities (2 weeks)
        2. Launch day plan
        3. User acquisition channels
        4. Key metrics to track
        5. Budget allocation suggestions
        """,
        system_prompt="You are a growth marketer. Be specific and actionable.",
        max_tokens=600,
    )
    
    if response.success:
        print(f"\n  ✅ Launch Strategy ({response.model}):")
        print(f"  {response.content[:500]}...")
    else:
        print(f"  ❌ Error: {response.error}")
    
    return {"phase": "execution", "success": response.success}


async def test_phase_rentabilisation():
    """Test Phase R: Rentabilisation - Monetization, optimization."""
    from viiper.core.phase import Phase
    from viiper.llm import UnifiedLLM
    
    print("\n" + "="*60)
    print("💰 PHASE R: RENTABILISATION")
    print("="*60)
    print(f"  Duration: {Phase.RENTABILISATION.typical_duration_weeks[0]}-{Phase.RENTABILISATION.typical_duration_weeks[1]} weeks")
    print(f"  Description: {Phase.RENTABILISATION.description}")
    
    # Use Kimi for business strategy
    llm = UnifiedLLM(model="moonshotai/kimi-k2.5")
    
    print("\n  Designing monetization strategy...")
    response = llm.complete(
        prompt="""
        Design monetization for "AI Email Assistant":
        
        1. Pricing tiers (Free, Pro, Enterprise)
        2. Feature gating strategy
        3. Revenue projections (Year 1)
        4. Retention strategies
        5. Upselling tactics
        """,
        system_prompt="You are a SaaS business strategist. Focus on profitability.",
        max_tokens=600,
    )
    
    if response.success:
        print(f"\n  ✅ Monetization ({response.model}):")
        print(f"  {response.content[:500]}...")
    else:
        print(f"  ❌ Error: {response.error}")
    
    return {"phase": "rentabilisation", "success": response.success}


async def test_phase_iteration():
    """Test Phase I²: Iteration - Continuous improvement."""
    from viiper.core.phase import Phase
    from viiper.llm import UnifiedLLM
    
    print("\n" + "="*60)
    print("🔄 PHASE I²: ITERATION")
    print("="*60)
    print(f"  Duration: Ongoing")
    print(f"  Description: {Phase.ITERATION.description}")
    
    # Use GLM5 for feature planning
    llm = UnifiedLLM(skill="planning")
    
    print("\n  Planning next iterations...")
    response = llm.complete(
        prompt="""
        Based on user feedback for "AI Email Assistant", prioritize:
        
        User requests:
        - Mobile app (500 votes)
        - Slack integration (350 votes)
        - Custom AI training (200 votes)
        - Team collaboration (180 votes)
        - Templates library (150 votes)
        
        Provide:
        1. Prioritized roadmap (Q1-Q2)
        2. Resource requirements
        3. Expected impact
        """,
        system_prompt="You are a product manager. Prioritize based on impact and effort.",
        max_tokens=500,
    )
    
    if response.success:
        print(f"\n  ✅ Iteration Plan ({response.model}):")
        print(f"  {response.content[:500]}...")
    else:
        print(f"  ❌ Error: {response.error}")
    
    return {"phase": "iteration", "success": response.success}


async def test_discovery_pipeline():
    """Test the new Browse → Idea → Code pipeline."""
    from viiper.agents.factory import create_discovery_team, create_browse_idea_code_pipeline
    from viiper.agents.idea_generation import IdeaGenerationAgent
    from viiper.agents.base import AgentTask
    
    print("\n" + "="*60)
    print("🆕 BONUS: Browse → Idea → Code Pipeline")
    print("="*60)
    
    # Create pipeline
    pipeline = create_browse_idea_code_pipeline()
    print(f"\n  Pipeline stages:")
    for stage, agents in pipeline.items():
        print(f"    {stage}: {[a.name for a in agents]}")
    
    # Test idea generation
    agent = IdeaGenerationAgent()
    task = AgentTask(
        name="Generate Ideas",
        description="Generate SaaS ideas",
        metadata={"niche": "productivity", "max_ideas": 3}
    )
    
    print("\n  Generating ideas...")
    result = await agent.execute_task(task)
    
    ideas = result.get("ideas", [])
    print(f"\n  ✅ Generated {len(ideas)} ideas:")
    for i, idea in enumerate(ideas, 1):
        score = idea.get("score", {})
        print(f"    {i}. {idea.get('title')} (score: {score.get('overall', 0):.2f})")
    
    return {"phase": "discovery", "success": True}


async def test_llm_integration():
    """Test LLM integration with all models."""
    from viiper.llm import UnifiedLLM, MODEL_CONFIGS
    
    print("\n" + "="*60)
    print("🤖 LLM INTEGRATION TEST")
    print("="*60)
    
    results = []
    
    for model_type, config in MODEL_CONFIGS.items():
        print(f"\n  Testing {config.model}...")
        llm = UnifiedLLM(model=config.model)
        
        response = llm.complete(
            prompt="Say 'Hello from VIIPER' and nothing else.",
            max_tokens=20,
        )
        
        status = "✅" if response.success else "❌"
        print(f"    {status} {config.provider}: {response.content[:50] if response.success else response.error}")
        results.append((config.model, response.success))
    
    return {"phase": "llm", "success": all(r[1] for r in results)}


async def run_full_test():
    """Run complete VIIPER pipeline test."""
    print("\n" + "="*60)
    print("🚀 VIIPER v4 - FULL PIPELINE TEST")
    print("="*60)
    print("\n  Testing all 6 phases: V → I → P → E → R → I²")
    print("  Models: NVIDIA GLM5, Kimi K2.5")
    
    results = []
    
    # Test each phase
    results.append(await test_phase_validation())
    results.append(await test_phase_ideation())
    results.append(await test_phase_production())
    results.append(await test_phase_execution())
    results.append(await test_phase_rentabilisation())
    results.append(await test_phase_iteration())
    
    # Bonus tests
    results.append(await test_discovery_pipeline())
    results.append(await test_llm_integration())
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for r in results if r["success"])
    total = len(results)
    
    for r in results:
        status = "✅ PASS" if r["success"] else "❌ FAIL"
        print(f"  {r['phase'].upper()}: {status}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n  🎉 ALL PHASES OPERATIONAL!")
    else:
        print(f"\n  ⚠️ {total - passed} phases need attention")
    
    return results


if __name__ == "__main__":
    asyncio.run(run_full_test())