"""
Tests for Phase 2 components.

Tests IterativeAgentLoop, EnhancedOrchestrator, and CollectiveKnowledgeBase.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio


class TestIterativeAgentLoop:
    """Tests for IterativeAgentLoop class."""

    def test_loop_creation(self):
        """Test that IterativeAgentLoop can be instantiated."""
        from viiper.orchestrator.iterative_loop import IterativeAgentLoop, LoopState
        
        # Create mock agent and task
        agent = MagicMock()
        task = MagicMock()
        task.name = "Test Task"
        task.description = "Test Description"
        
        loop = IterativeAgentLoop(agent=agent, task=task)
        
        assert loop.state == LoopState.IDLE
        assert loop.max_steps == IterativeAgentLoop.ORCHESTRATOR_MAX_STEPS
        assert loop.current_step == 0

    def test_loop_step_limits(self):
        """Test step limits for orchestrator and sub-agents."""
        from viiper.orchestrator.iterative_loop import IterativeAgentLoop
        
        assert IterativeAgentLoop.ORCHESTRATOR_MAX_STEPS == 15
        assert IterativeAgentLoop.SUB_AGENT_MAX_STEPS == 100

    def test_loop_state_enum(self):
        """Test LoopState enum values."""
        from viiper.orchestrator.iterative_loop import LoopState
        
        assert LoopState.IDLE.value == "idle"
        assert LoopState.ANALYZING.value == "analyzing"
        assert LoopState.PLANNING.value == "planning"
        assert LoopState.EXECUTING.value == "executing"
        assert LoopState.OBSERVING.value == "observing"
        assert LoopState.LEARNING.value == "learning"
        assert LoopState.COMPLETED.value == "completed"
        assert LoopState.FAILED.value == "failed"

    def test_step_result_model(self):
        """Test StepResult model."""
        from viiper.orchestrator.iterative_loop import StepResult
        
        result = StepResult(
            step_number=1,
            action="test_action",
            success=True,
            output={"key": "value"},
        )
        
        assert result.step_number == 1
        assert result.action == "test_action"
        assert result.success is True

    def test_loop_metrics_model(self):
        """Test LoopMetrics model."""
        from viiper.orchestrator.iterative_loop import LoopMetrics
        
        metrics = LoopMetrics(
            total_steps=10,
            successful_steps=8,
            failed_steps=2,
            total_duration_seconds=5.5,
        )
        
        assert metrics.total_steps == 10
        assert metrics.successful_steps == 8
        assert metrics.failed_steps == 2


class TestSubAgentSpawner:
    """Tests for SubAgentSpawner class."""

    def test_spawner_creation(self):
        """Test SubAgentSpawner instantiation."""
        from viiper.orchestrator.enhanced_orchestrator import SubAgentSpawner
        
        spawner = SubAgentSpawner(max_sub_agents=10)
        
        assert spawner.max_sub_agents == 10
        assert len(spawner.active_sub_agents) == 0

    def test_spawn_agent(self):
        """Test spawning an agent."""
        from viiper.orchestrator.enhanced_orchestrator import SubAgentSpawner
        
        spawner = SubAgentSpawner(max_sub_agents=2)
        
        # Mock AgentFactory
        with patch('viiper.orchestrator.enhanced_orchestrator.AgentFactory') as mock_factory:
            mock_agent = MagicMock()
            mock_agent.name = "test_agent"
            mock_factory.create_agent.return_value = mock_agent
            
            agent = spawner.spawn_agent("browser", "parent_123")
            
            assert agent is not None
            assert spawner.get_active_count() == 1

    def test_max_sub_agents_limit(self):
        """Test that spawner respects max limit."""
        from viiper.orchestrator.enhanced_orchestrator import SubAgentSpawner
        
        spawner = SubAgentSpawner(max_sub_agents=1)
        
        with patch('viiper.orchestrator.enhanced_orchestrator.AgentFactory') as mock_factory:
            mock_agent = MagicMock()
            mock_factory.create_agent.return_value = mock_agent
            
            # First spawn should succeed
            agent1 = spawner.spawn_agent("browser", "parent_123")
            assert agent1 is not None
            
            # Second spawn should fail (limit reached)
            agent2 = spawner.spawn_agent("backend", "parent_123")
            assert agent2 is None


class TestParallelExecutor:
    """Tests for ParallelExecutor class."""

    def test_executor_creation(self):
        """Test ParallelExecutor instantiation."""
        from viiper.orchestrator.enhanced_orchestrator import ParallelExecutor
        
        executor = ParallelExecutor(max_concurrent=5)
        
        assert executor.max_concurrent == 5

    @pytest.mark.asyncio
    async def test_parallel_execution(self):
        """Test parallel task execution."""
        from viiper.orchestrator.enhanced_orchestrator import ParallelExecutor
        from viiper.agents.base import AgentTask
        
        executor = ParallelExecutor(max_concurrent=2)
        
        # Create mock tasks and agents
        task1 = AgentTask(name="Task 1", description="Test 1")
        task2 = AgentTask(name="Task 2", description="Test 2")
        
        mock_agent = MagicMock()
        mock_agent.status = "idle"
        mock_agent.execute_task = AsyncMock(return_value={"success": True})
        
        results = await executor.execute_parallel([task1, task2], [mock_agent])
        
        assert len(results) == 2


class TestErrorRecovery:
    """Tests for ErrorRecovery class."""

    def test_recovery_creation(self):
        """Test ErrorRecovery instantiation."""
        from viiper.orchestrator.enhanced_orchestrator import ErrorRecovery
        
        recovery = ErrorRecovery(max_retries=3, backoff_factor=2.0)
        
        assert recovery.max_retries == 3
        assert recovery.backoff_factor == 2.0

    @pytest.mark.asyncio
    async def test_retry_on_failure(self):
        """Test retry logic on failure."""
        from viiper.orchestrator.enhanced_orchestrator import ErrorRecovery
        from viiper.agents.base import AgentTask
        
        recovery = ErrorRecovery(max_retries=2, backoff_factor=1.0)
        
        task = AgentTask(name="Test", description="Test")
        
        mock_agent = MagicMock()
        mock_agent.assign_task = MagicMock()
        mock_agent.fail_task = MagicMock()
        mock_agent.complete_task = MagicMock()
        
        # Always fails
        mock_agent.execute_task = AsyncMock(return_value={"success": False, "error": "Failed"})
        
        result = await recovery.execute_with_retry(task, mock_agent)
        
        assert result["success"] is False
        assert result["retries"] == 2


class TestCollectiveKnowledgeBase:
    """Tests for CollectiveKnowledgeBase class."""

    def test_ckb_creation(self):
        """Test CKB instantiation."""
        from viiper.ckb.collective_knowledge import CollectiveKnowledgeBase
        
        ckb = CollectiveKnowledgeBase()
        
        assert len(ckb.knowledge) == 0
        assert len(ckb.patterns) == 0
        assert len(ckb.learnings) == 0

    def test_contribute_knowledge(self):
        """Test contributing knowledge."""
        from viiper.ckb.collective_knowledge import CollectiveKnowledgeBase, KnowledgeType
        
        ckb = CollectiveKnowledgeBase()
        
        entry = ckb.contribute(
            type=KnowledgeType.PATTERN,
            title="Test Pattern",
            content={"description": "A test pattern"},
            tags=["test", "pattern"],
            source_agent="TestAgent",
        )
        
        assert entry.title == "Test Pattern"
        assert len(ckb.knowledge) == 1

    def test_search_knowledge(self):
        """Test searching knowledge."""
        from viiper.ckb.collective_knowledge import CollectiveKnowledgeBase, KnowledgeType
        
        ckb = CollectiveKnowledgeBase()
        
        # Add some knowledge
        ckb.contribute(
            type=KnowledgeType.PATTERN,
            title="API Pattern",
            content={"description": "REST API pattern"},
            tags=["api", "rest"],
        )
        
        ckb.contribute(
            type=KnowledgeType.BEST_PRACTICE,
            title="Security Best Practice",
            content={"description": "HTTPS everywhere"},
            tags=["security"],
        )
        
        # Search for API
        results = ckb.search("API")
        assert len(results) == 1
        assert results[0].title == "API Pattern"
        
        # Search for security
        results = ckb.search("security")
        assert len(results) == 1
        assert results[0].title == "Security Best Practice"

    def test_contribute_pattern(self):
        """Test contributing a pattern."""
        from viiper.ckb.collective_knowledge import CollectiveKnowledgeBase, KnowledgeType
        
        ckb = CollectiveKnowledgeBase()
        
        entry = ckb.contribute(
            type=KnowledgeType.PATTERN,
            title="Retry Pattern",
            content={
                "description": "Retry failed requests",
                "triggers": ["error", "timeout"],
                "actions": [{"type": "retry", "delay": 1}],
            },
            tags=["resilience"],
        )
        
        assert len(ckb.patterns) == 1
        assert "Retry Pattern" in ckb.patterns[entry.id].name

    def test_contribute_learning(self):
        """Test contributing a learning."""
        from viiper.ckb.collective_knowledge import CollectiveKnowledgeBase, KnowledgeType
        
        ckb = CollectiveKnowledgeBase()
        
        ckb.contribute(
            type=KnowledgeType.LEARNING,
            title="Agent Learning",
            content={
                "context": {"agent": "FrontendAgent"},
                "observation": "Tailwind works well",
                "insight": "Use utility-first CSS",
                "adjustment": "Default to Tailwind",
            },
        )
        
        assert len(ckb.learnings) == 1

    def test_get_patterns_for_context(self):
        """Test getting patterns for context."""
        from viiper.ckb.collective_knowledge import CollectiveKnowledgeBase, KnowledgeType
        
        ckb = CollectiveKnowledgeBase()
        
        ckb.contribute(
            type=KnowledgeType.PATTERN,
            title="Error Handling",
            content={
                "description": "Handle API errors",
                "triggers": ["api", "error"],
                "actions": [{"type": "retry"}],
            },
        )
        
        patterns = ckb.get_patterns_for_context({"type": "api_error"})
        assert len(patterns) == 1

    def test_usage_recording(self):
        """Test usage recording."""
        from viiper.ckb.collective_knowledge import CollectiveKnowledgeBase, KnowledgeType
        
        ckb = CollectiveKnowledgeBase()
        
        entry = ckb.contribute(
            type=KnowledgeType.PATTERN,
            title="Test",
            content={},
        )
        
        # Record successful usage
        ckb.record_usage(entry.id, success=True)
        assert ckb.knowledge[entry.id].usage_count == 1
        assert ckb.knowledge[entry.id].success_rate == 1.0
        
        # Record failed usage
        ckb.record_usage(entry.id, success=False)
        assert ckb.knowledge[entry.id].usage_count == 2
        assert ckb.knowledge[entry.id].success_rate == 0.5

    def test_get_stats(self):
        """Test getting CKB statistics."""
        from viiper.ckb.collective_knowledge import CollectiveKnowledgeBase, KnowledgeType
        
        ckb = CollectiveKnowledgeBase()
        
        ckb.contribute(KnowledgeType.PATTERN, "Pattern 1", {})
        ckb.contribute(KnowledgeType.LEARNING, "Learning 1", {})
        
        stats = ckb.get_stats()
        
        assert stats["total_entries"] == 2
        assert stats["patterns"] == 1
        assert stats["learnings"] == 1

    def test_export_import(self):
        """Test exporting and importing knowledge."""
        from viiper.ckb.collective_knowledge import CollectiveKnowledgeBase, KnowledgeType
        
        ckb1 = CollectiveKnowledgeBase()
        
        ckb1.contribute(
            type=KnowledgeType.PATTERN,
            title="Test Pattern",
            content={"key": "value"},
            tags=["test"],
        )
        
        # Export
        exported = ckb1.export_knowledge()
        
        # Import into new CKB
        ckb2 = CollectiveKnowledgeBase()
        ckb2.import_knowledge(exported)
        
        assert len(ckb2.knowledge) == 1
        assert len(ckb2.patterns) == 1


class TestGlobalCKB:
    """Tests for global CKB functions."""

    def test_get_ckb(self):
        """Test get_ckb returns singleton."""
        from viiper.ckb.collective_knowledge import get_ckb
        
        ckb1 = get_ckb()
        ckb2 = get_ckb()
        
        assert ckb1 is ckb2

    def test_contribute_knowledge_function(self):
        """Test contribute_knowledge helper."""
        from viiper.ckb.collective_knowledge import (
            contribute_knowledge,
            get_ckb,
            KnowledgeType,
        )
        
        # Clear CKB
        ckb = get_ckb()
        ckb.knowledge.clear()
        ckb.patterns.clear()
        ckb.learnings.clear()
        
        entry = contribute_knowledge(
            type=KnowledgeType.BEST_PRACTICE,
            title="Test Best Practice",
            content={"description": "A test"},
        )
        
        assert entry is not None


# Run with: pytest tests/unit/test_phase2.py -v