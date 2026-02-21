"""
Full Pipeline Integration Test.

Tests the complete Browse → Idea → Code pipeline with all agents and phases.
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


async def test_agent_instantiation():
    """Test that all agents can be instantiated."""
    from viiper.agents.factory import AgentFactory, AgentRegistry
    
    print("\n" + "="*60)
    print("🧪 TEST 1: Agent Instantiation")
    print("="*60)
    
    all_agents = AgentRegistry.list_all_agents()
    results = {}
    
    for agent_name in all_agents:
        try:
            agent = AgentFactory.create_agent(agent_name)
            if agent:
                results[agent_name] = {
                    "success": True,
                    "name": agent.name,
                    "role": agent.role.value,
                    "capabilities": len(agent.capabilities),
                    "skills": len(agent.skills)
                }
                print(f"  ✅ {agent_name}: {agent.name} ({agent.role.value})")
            else:
                results[agent_name] = {"success": False, "error": "Agent is None"}
                print(f"  ❌ {agent_name}: Agent is None")
        except Exception as e:
            results[agent_name] = {"success": False, "error": str(e)}
            print(f"  ❌ {agent_name}: {str(e)}")
    
    success_count = sum(1 for r in results.values() if r["success"])
    print(f"\n📊 Results: {success_count}/{len(all_agents)} agents instantiated")
    
    return results


async def test_agent_capabilities():
    """Test that agents have proper capabilities."""
    from viiper.agents import (
        BrowserAgent, IdeaGenerationAgent,
        SystemDesignAgent, TechStackAgent, SecurityPlanningAgent,
        FrontendAgent, BackendAgent, TestingAgent, DevOpsAgent,
        AgentCapability
    )
    
    print("\n" + "="*60)
    print("🧪 TEST 2: Agent Capabilities")
    print("="*60)
    
    results = {}
    
    # Test BrowserAgent
    try:
        browser = BrowserAgent()
        results["BrowserAgent"] = {
            "success": True,
            "capabilities": [c.value for c in browser.capabilities],
            "has_navigation": hasattr(browser, '_navigate'),
            "has_search": hasattr(browser, '_search'),
        }
        print(f"  ✅ BrowserAgent: {len(browser.capabilities)} capabilities")
    except Exception as e:
        results["BrowserAgent"] = {"success": False, "error": str(e)}
        print(f"  ❌ BrowserAgent: {str(e)}")
    
    # Test IdeaGenerationAgent
    try:
        idea_gen = IdeaGenerationAgent()
        results["IdeaGenerationAgent"] = {
            "success": True,
            "capabilities": [c.value for c in idea_gen.capabilities],
            "has_score_method": hasattr(idea_gen, '_score_ideas'),
            "has_trend_method": hasattr(idea_gen, '_gather_trends'),
        }
        print(f"  ✅ IdeaGenerationAgent: {len(idea_gen.capabilities)} capabilities")
    except Exception as e:
        results["IdeaGenerationAgent"] = {"success": False, "error": str(e)}
        print(f"  ❌ IdeaGenerationAgent: {str(e)}")
    
    # Test Architecture Agents
    for AgentClass in [SystemDesignAgent, TechStackAgent, SecurityPlanningAgent]:
        try:
            agent = AgentClass()
            results[agent.name] = {
                "success": True,
                "capabilities": len(agent.capabilities),
            }
            print(f"  ✅ {agent.name}: {len(agent.capabilities)} capabilities")
        except Exception as e:
            results[AgentClass.__name__] = {"success": False, "error": str(e)}
            print(f"  ❌ {AgentClass.__name__}: {str(e)}")
    
    # Test Production Agents
    for AgentClass in [FrontendAgent, BackendAgent, TestingAgent, DevOpsAgent]:
        try:
            agent = AgentClass()
            results[agent.name] = {
                "success": True,
                "capabilities": len(agent.capabilities),
            }
            print(f"  ✅ {agent.name}: {len(agent.capabilities)} capabilities")
        except Exception as e:
            results[AgentClass.__name__] = {"success": False, "error": str(e)}
            print(f"  ❌ {AgentClass.__name__}: {str(e)}")
    
    success_count = sum(1 for r in results.values() if r["success"])
    print(f"\n📊 Results: {success_count}/{len(results)} agents tested")
    
    return results


async def test_orchestrator():
    """Test orchestrator functionality."""
    from viiper.core.project import Project
    from viiper.orchestrator import ProjectOrchestrator, EnhancedOrchestrator
    
    print("\n" + "="*60)
    print("🧪 TEST 3: Orchestrator")
    print("="*60)
    
    results = {}
    
    # Create test project
    try:
        project = Project(name="Test Project", variant="saas")
        print(f"  ✅ Project created: {project.name}")
    except Exception as e:
        print(f"  ❌ Project creation failed: {str(e)}")
        return {"success": False, "error": str(e)}
    
    # Test ProjectOrchestrator
    try:
        orchestrator = ProjectOrchestrator(project, auto_register_agents=True)
        status = orchestrator.get_status()
        results["ProjectOrchestrator"] = {
            "success": True,
            "agents_registered": status["agents_registered"],
            "project_health": status["project_health"],
        }
        print(f"  ✅ ProjectOrchestrator: {status['agents_registered']} agents registered")
    except Exception as e:
        results["ProjectOrchestrator"] = {"success": False, "error": str(e)}
        print(f"  ❌ ProjectOrchestrator: {str(e)}")
    
    # Test EnhancedOrchestrator
    try:
        enhanced = EnhancedOrchestrator(
            project,
            max_sub_agents=5,
            max_parallel_tasks=3,
            auto_register_agents=True
        )
        status = enhanced.get_enhanced_status()
        results["EnhancedOrchestrator"] = {
            "success": True,
            "agents_registered": status["agents_registered"],
            "sub_agents_capacity": status["parallel_tasks_capacity"],
        }
        print(f"  ✅ EnhancedOrchestrator: {status['agents_registered']} agents, {status['parallel_tasks_capacity']} parallel capacity")
    except Exception as e:
        results["EnhancedOrchestrator"] = {"success": False, "error": str(e)}
        print(f"  ❌ EnhancedOrchestrator: {str(e)}")
    
    return results


async def test_iterative_loop():
    """Test IterativeAgentLoop."""
    from viiper.orchestrator.iterative_loop import IterativeAgentLoop, LoopState
    from viiper.agents.base import AgentTask
    from viiper.agents.factory import AgentFactory
    
    print("\n" + "="*60)
    print("🧪 TEST 4: Iterative Agent Loop")
    print("="*60)
    
    results = {}
    
    # Create a simple test agent
    try:
        agent = AgentFactory.create_agent("market_research")
        if not agent:
            print("  ❌ Could not create agent")
            return {"success": False, "error": "Agent creation failed"}
        
        # Create a simple task
        task = AgentTask(
            name="Test Task",
            description="A simple test task",
            metadata={"test": True}
        )
        
        # Create loop with max 3 steps for testing
        loop = IterativeAgentLoop(
            agent=agent,
            task=task,
            max_steps=3
        )
        
        results["loop_creation"] = {
            "success": True,
            "initial_state": loop.state.value,
            "max_steps": loop.max_steps,
        }
        print(f"  ✅ Loop created: state={loop.state.value}, max_steps={loop.max_steps}")
        
        # Test loop components
        results["loop_components"] = {
            "success": True,
            "has_analyze": hasattr(loop, '_analyze'),
            "has_plan": hasattr(loop, '_plan'),
            "has_execute": hasattr(loop, '_execute'),
            "has_observe": hasattr(loop, '_observe'),
            "has_learn": hasattr(loop, '_learn'),
        }
        print(f"  ✅ Loop components verified")
        
    except Exception as e:
        results["loop_creation"] = {"success": False, "error": str(e)}
        print(f"  ❌ Loop creation failed: {str(e)}")
    
    return results


async def test_collective_knowledge_base():
    """Test CollectiveKnowledgeBase."""
    from viiper.ckb import CollectiveKnowledgeBase, KnowledgeType
    
    print("\n" + "="*60)
    print("🧪 TEST 5: Collective Knowledge Base")
    print("="*60)
    
    results = {}
    
    try:
        ckb = CollectiveKnowledgeBase()
        
        # Test contribution
        entry = ckb.contribute(
            type=KnowledgeType.PATTERN,
            title="Test Pattern",
            content={"description": "A test pattern"},
            tags=["test"],
            source_agent="TestAgent",
        )
        results["contribute"] = {
            "success": True,
            "entry_id": entry.id,
        }
        print(f"  ✅ Knowledge contributed: {entry.id}")
        
        # Test search
        search_results = ckb.search("test")
        results["search"] = {
            "success": True,
            "results_count": len(search_results),
        }
        print(f"  ✅ Search found: {len(search_results)} results")
        
        # Test stats
        stats = ckb.get_stats()
        results["stats"] = {
            "success": True,
            "total_entries": stats["total_entries"],
        }
        print(f"  ✅ Stats: {stats['total_entries']} entries")
        
    except Exception as e:
        results["ckb"] = {"success": False, "error": str(e)}
        print(f"  ❌ CKB failed: {str(e)}")
    
    return results


async def test_idea_generation():
    """Test IdeaGenerationAgent without browser."""
    from viiper.agents.idea_generation import IdeaGenerationAgent, IdeaCategory
    from viiper.agents.base import AgentTask
    
    print("\n" + "="*60)
    print("🧪 TEST 6: Idea Generation")
    print("="*60)
    
    results = {}
    
    try:
        agent = IdeaGenerationAgent()
        
        # Test keyword extraction
        keywords = agent._extract_keywords("AI automation productivity workflow")
        results["keyword_extraction"] = {
            "success": True,
            "keywords": keywords,
        }
        print(f"  ✅ Keywords extracted: {keywords}")
        
        # Test pain points
        pain_points = agent._identify_pain_points("I wish there was an easier way to do this")
        results["pain_points"] = {
            "success": True,
            "count": len(pain_points),
        }
        print(f"  ✅ Pain points found: {len(pain_points)}")
        
        # Test market gaps
        gaps = agent._find_market_gaps([])
        results["market_gaps"] = {
            "success": True,
            "count": len(gaps),
        }
        print(f"  ✅ Market gaps found: {len(gaps)}")
        
        # Test idea scoring
        from viiper.agents.idea_generation import AppIdea, IdeaScore
        test_idea = AppIdea(
            id="test",
            title="Test SaaS",
            description="Test",
            category=IdeaCategory.SAAS,
            monetization=["Subscription", "Usage"],
            competitors=["A", "B"],
            key_features=["Feature 1", "Feature 2"],
        )
        
        market_size = agent._estimate_market_size(test_idea)
        competition = agent._estimate_competition(test_idea)
        
        results["idea_scoring"] = {
            "success": True,
            "market_size": market_size,
            "competition": competition,
        }
        print(f"  ✅ Idea scoring: market_size={market_size}, competition={competition}")
        
    except Exception as e:
        results["idea_generation"] = {"success": False, "error": str(e)}
        print(f"  ❌ Idea generation failed: {str(e)}")
    
    return results


async def test_collaboration():
    """Test agent collaboration system."""
    from viiper.agents.collaboration import (
        CollaborationProtocol, MessageType, SharedContext
    )
    
    print("\n" + "="*60)
    print("🧪 TEST 7: Agent Collaboration")
    print("="*60)
    
    results = {}
    
    try:
        protocol = CollaborationProtocol()
        
        # Test context creation
        context = protocol.create_context(
            project_id="test-project",
            phase="ideation",
            variant="saas"
        )
        results["context_creation"] = {
            "success": True,
            "project_id": context.project_id,
        }
        print(f"  ✅ Context created: {context.project_id}")
        
        # Test message passing
        msg = protocol.send_message(
            from_agent="SystemDesignAgent",
            to_agent="TechStackAgent",
            message_type=MessageType.REQUEST,
            subject="Need architecture",
            content={"query": "What tech stack?"},
        )
        results["messaging"] = {
            "success": True,
            "message_id": msg.id,
        }
        print(f"  ✅ Message sent: {msg.id}")
        
        # Test context sharing
        protocol.share_context("test-project", "System Design Agent", {"architecture": "microservices"})
        results["context_sharing"] = {
            "success": True,
            "context_updated": context.updated_at is not None,
        }
        print(f"  ✅ Context shared")
        
    except Exception as e:
        results["collaboration"] = {"success": False, "error": str(e)}
        print(f"  ❌ Collaboration failed: {str(e)}")
    
    return results


async def run_all_tests():
    """Run all integration tests."""
    print("\n" + "="*60)
    print("🚀 VIIPER FULL PIPELINE TEST SUITE")
    print("="*60)
    
    all_results = {}
    
    # Run all tests
    all_results["agent_instantiation"] = await test_agent_instantiation()
    all_results["agent_capabilities"] = await test_agent_capabilities()
    all_results["orchestrator"] = await test_orchestrator()
    all_results["iterative_loop"] = await test_iterative_loop()
    all_results["ckb"] = await test_collective_knowledge_base()
    all_results["idea_generation"] = await test_idea_generation()
    all_results["collaboration"] = await test_collaboration()
    
    # Calculate overall success rate
    total_tests = len(all_results)
    successful_tests = sum(
        1 for r in all_results.values()
        if any(v.get("success", False) for v in r.values() if isinstance(v, dict))
    )
    
    print("\n" + "="*60)
    print("📊 FINAL RESULTS")
    print("="*60)
    print(f"Total test suites: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Success rate: {successful_tests/total_tests*100:.1f}%")
    
    return all_results


if __name__ == "__main__":
    asyncio.run(run_all_tests())