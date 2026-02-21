"""
Test NVIDIA LLM Integration with VIIPER.

Demonstrates how to use NVIDIA's AI models with VIIPER agents.
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_basic_completion():
    """Test basic completion with NVIDIA LLM."""
    from viiper.llm import NvidiaLLM
    
    print("\n" + "="*60)
    print("🤖 TEST 1: Basic Completion")
    print("="*60)
    
    llm = NvidiaLLM()
    
    print("  Sending prompt to z-ai/glm5...")
    response = llm.complete(
        prompt="What are 3 key trends in SaaS for 2026?",
        max_tokens=500,
    )
    
    if response.success:
        print(f"\n  ✅ Response ({response.tokens_used} tokens):")
        print(f"  {response.content[:300]}...")
        if response.reasoning:
            print(f"\n  💭 Reasoning: {response.reasoning[:200]}...")
    else:
        print(f"  ❌ Error: {response.error}")
    
    return response


def test_code_generation():
    """Test code generation with NVIDIA LLM."""
    from viiper.llm import NvidiaLLM
    
    print("\n" + "="*60)
    print("💻 TEST 2: Code Generation")
    print("="*60)
    
    llm = NvidiaLLM()
    
    print("  Generating Python code...")
    response = llm.generate_code(
        description="A function that validates email addresses using regex",
        language="python",
    )
    
    if response.success:
        print(f"\n  ✅ Generated code:")
        print(f"  {response.content[:500]}...")
    else:
        print(f"  ❌ Error: {response.error}")
    
    return response


def test_architecture_design():
    """Test architecture design with NVIDIA LLM."""
    from viiper.llm import NvidiaLLM
    
    print("\n" + "="*60)
    print("🏗️ TEST 3: Architecture Design")
    print("="*60)
    
    llm = NvidiaLLM()
    
    print("  Designing system architecture...")
    response = llm.design_architecture(
        requirements="A real-time collaboration platform for remote teams with video chat, document sharing, and task management",
        constraints=[
            "Must scale to 10,000 concurrent users",
            "Latency under 100ms for real-time features",
            "GDPR compliant",
        ],
    )
    
    if response.success:
        print(f"\n  ✅ Architecture design:")
        print(f"  {response.content[:500]}...")
    else:
        print(f"  ❌ Error: {response.error}")
    
    return response


def test_market_analysis():
    """Test market trend analysis with NVIDIA LLM."""
    from viiper.llm import NvidiaLLM
    
    print("\n" + "="*60)
    print("📊 TEST 4: Market Analysis")
    print("="*60)
    
    llm = NvidiaLLM()
    
    market_data = """
    Product Hunt Trends (Feb 2026):
    - AI writing assistants: +45% growth
    - No-code platforms: +32% growth
    - Privacy-focused tools: +28% growth
    - Developer productivity: +25% growth
    
    Reddit r/SaaS hot topics:
    - Micro-SaaS pricing strategies
    - AI integration for small teams
    - First-time founder mistakes to avoid
    """
    
    print("  Analyzing market trends...")
    response = llm.analyze_market_trends(market_data)
    
    if response.success:
        print(f"\n  ✅ Analysis:")
        print(f"  {response.content[:400]}...")
    else:
        print(f"  ❌ Error: {response.error}")
    
    return response


def test_streaming():
    """Test streaming response with NVIDIA LLM."""
    from viiper.llm import NvidiaLLM
    
    print("\n" + "="*60)
    print("⚡ TEST 5: Streaming Response")
    print("="*60)
    
    llm = NvidiaLLM()
    
    print("  Streaming response (with reasoning)...")
    print("\n  --- Response ---")
    
    response = llm.complete(
        prompt="Explain the concept of 'product-market fit' in 3 sentences.",
        max_tokens=200,
        stream=True,
    )
    
    print("\n  --- End ---")
    
    return response


def test_with_supabase_context():
    """Test LLM with Supabase project context."""
    from viiper.llm import NvidiaLLM
    
    print("\n" + "="*60)
    print("🗄️ TEST 6: Supabase Project Analysis")
    print("="*60)
    
    llm = NvidiaLLM()
    
    prompt = """
    I have a Supabase project called 'Contente_créator' for content creation.
    
    Suggest:
    1. Database schema for content management
    2. Key features to implement
    3. Monetization strategies
    
    Focus on AI-powered content generation capabilities.
    """
    
    print("  Analyzing Supabase project...")
    response = llm.complete(
        prompt=prompt,
        system_prompt="You are a startup advisor and software architect. Be concise and actionable.",
        max_tokens=800,
    )
    
    if response.success:
        print(f"\n  ✅ Recommendations:")
        print(f"  {response.content[:600]}...")
    else:
        print(f"  ❌ Error: {response.error}")
    
    return response


def main():
    print("\n" + "="*60)
    print("🚀 VIIPER + NVIDIA LLM Integration Test")
    print("="*60)
    
    # Run tests
    test_basic_completion()
    test_code_generation()
    test_architecture_design()
    test_market_analysis()
    test_streaming()
    test_with_supabase_context()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETE!")
    print("="*60)
    print("\n  NVIDIA LLM is now integrated with VIIPER agents.")
    print("  Use 'from viiper.llm import get_llm' to access.")


if __name__ == "__main__":
    main()