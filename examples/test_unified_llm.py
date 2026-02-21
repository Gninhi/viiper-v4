"""
Test Unified LLM Interface with multiple models.

Tests NVIDIA GLM5 and Kimi K2.5 with skill-based routing.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_model_configs():
    """Test model configurations."""
    from viiper.llm import MODEL_CONFIGS, ModelType
    
    print("\n" + "="*60)
    print("📋 TEST 1: Model Configurations")
    print("="*60)
    
    for model_type, config in MODEL_CONFIGS.items():
        print(f"\n  {config.model}:")
        print(f"    Provider: {config.provider}")
        print(f"    Max tokens: {config.max_tokens}")
        print(f"    Thinking: {config.supports_thinking}")
        print(f"    Best for: {', '.join(config.best_for)}")
    
    return True


def test_skill_routing():
    """Test skill-based model routing."""
    from viiper.llm import UnifiedLLM
    
    print("\n" + "="*60)
    print("🎯 TEST 2: Skill-Based Routing")
    print("="*60)
    
    llm = UnifiedLLM()
    
    skills = ["code_generation", "market_research", "architecture", "idea_generation"]
    
    for skill in skills:
        model = llm.select_model_for_skill(skill)
        print(f"  {skill} → {model}")
    
    return True


def test_kimi_k25():
    """Test Kimi K2.5 model."""
    from viiper.llm import UnifiedLLM
    
    print("\n" + "="*60)
    print("🌙 TEST 3: Kimi K2.5 - Market Analysis")
    print("="*60)
    
    llm = UnifiedLLM(model="moonshotai/kimi-k2.5")
    
    print("  Sending prompt to Kimi K2.5...")
    response = llm.complete(
        prompt="What are 3 emerging SaaS trends in 2026?",
        max_tokens=300,
    )
    
    if response.success:
        print(f"\n  ✅ Response from {response.model}:")
        print(f"  {response.content[:300]}...")
    else:
        print(f"  ❌ Error: {response.error}")
    
    return response.success


def test_glm5():
    """Test GLM5 model for code generation."""
    from viiper.llm import UnifiedLLM
    
    print("\n" + "="*60)
    print("🤖 TEST 4: GLM5 - Code Generation")
    print("="*60)
    
    llm = UnifiedLLM(model="z-ai/glm5")
    
    print("  Generating Python code...")
    response = llm.generate_code(
        description="A function that calculates Fibonacci numbers"
    )
    
    if response.success:
        print(f"\n  ✅ Generated code:")
        print(f"  {response.content[:400]}...")
    else:
        print(f"  ❌ Error: {response.error}")
    
    return response.success


def test_auto_routing():
    """Test automatic model selection based on skill."""
    from viiper.llm import UnifiedLLM
    
    print("\n" + "="*60)
    print("🔀 TEST 5: Auto Model Selection")
    print("="*60)
    
    # Code generation should use GLM5
    llm_code = UnifiedLLM(skill="code_generation")
    config = llm_code.get_config()
    print(f"  Code generation → {config.model}")
    
    # Market research should use Kimi K2.5
    llm_market = UnifiedLLM(skill="market_research")
    config = llm_market.get_config()
    print(f"  Market research → {config.model}")
    
    return True


def test_idea_generation_with_kimi():
    """Test idea generation using Kimi K2.5."""
    from viiper.llm import UnifiedLLM
    
    print("\n" + "="*60)
    print("💡 TEST 6: Idea Generation (Kimi K2.5)")
    print("="*60)
    
    llm = UnifiedLLM()
    
    context = """
    Market trends:
    - AI automation growing 45% YoY
    - No-code platforms gaining traction
    - Privacy-first tools in demand
    """
    
    print("  Generating ideas with Kimi K2.5...")
    response = llm.generate_ideas(context)
    
    if response.success:
        print(f"\n  ✅ Ideas from {response.model}:")
        print(f"  {response.content[:400]}...")
    else:
        print(f"  ❌ Error: {response.error}")
    
    return response.success


def test_streaming():
    """Test streaming response."""
    from viiper.llm import UnifiedLLM
    
    print("\n" + "="*60)
    print("⚡ TEST 7: Streaming Response")
    print("="*60)
    
    llm = UnifiedLLM(stream=True)
    
    print("  Streaming from GLM5...")
    response = llm.complete(
        prompt="Explain the concept of micro-SaaS in 2 sentences.",
        max_tokens=100,
    )
    
    return response.success


def main():
    print("\n" + "="*60)
    print("🚀 VIIPER Unified LLM Test Suite")
    print("="*60)
    print("\n  Testing NVIDIA GLM5 + Kimi K2.5 integration")
    
    # Run tests
    results = []
    
    results.append(("Model Configs", test_model_configs()))
    results.append(("Skill Routing", test_skill_routing()))
    results.append(("Kimi K2.5", test_kimi_k25()))
    results.append(("GLM5 Code", test_glm5()))
    results.append(("Auto Routing", test_auto_routing()))
    results.append(("Idea Generation", test_idea_generation_with_kimi()))
    results.append(("Streaming", test_streaming()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name}: {status}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n  🎉 ALL TESTS PASSED!")
    
    print("\n" + "="*60)
    print("  USAGE EXAMPLES")
    print("="*60)
    print("""
  from viiper.llm import UnifiedLLM, get_llm
  
  # Auto-select model based on skill
  llm = UnifiedLLM(skill="code_generation")
  response = llm.complete("Write a Python function")
  
  # Use specific model
  llm = UnifiedLLM(model="moonshotai/kimi-k2.5")
  response = llm.generate_ideas("AI productivity tools")
  
  # Quick helper
  from viiper.llm import complete
  result = complete("Hello!", model="z-ai/glm5")
    """)


if __name__ == "__main__":
    main()