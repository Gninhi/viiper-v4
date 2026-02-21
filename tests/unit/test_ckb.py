"""
Tests for Collective Knowledge Base (CKB).
"""

import pytest
from datetime import datetime
import tempfile
import os

from viiper.ckb import (
    KnowledgeEntry,
    KnowledgeType,
    KnowledgeSource,
    CollectiveKnowledgeBase,
    SimpleVectorStore,
    add_knowledge,
    search_knowledge,
    get_knowledge_stats,
    collective_kb,
)


# =============================================================================
# KNOWLEDGE ENTRY TESTS
# =============================================================================


class TestKnowledgeEntry:
    """Test KnowledgeEntry dataclass."""

    def test_entry_creation(self):
        """Test basic entry creation."""
        entry = KnowledgeEntry(
            id="",
            type=KnowledgeType.PATTERN,
            title="Test Pattern",
            content="This is a test pattern",
            tags=["test", "pattern"],
        )

        assert entry.title == "Test Pattern"
        assert entry.type == KnowledgeType.PATTERN
        assert len(entry.tags) == 2
        assert entry.id != ""  # Auto-generated

    def test_entry_id_generation(self):
        """Test ID generation from content."""
        entry1 = KnowledgeEntry(
            id="",
            type=KnowledgeType.LESSON,
            title="Lesson 1",
            content="Content A",
        )

        entry2 = KnowledgeEntry(
            id="",
            type=KnowledgeType.LESSON,
            title="Lesson 1",
            content="Content B",  # Different content
        )

        # Different content should generate different IDs
        assert entry1.id != entry2.id
        # But both should have valid IDs
        assert entry1.id.startswith("lesson_")
        assert entry2.id.startswith("lesson_")

    def test_entry_usage_increment(self):
        """Test usage counter."""
        entry = KnowledgeEntry(
            id="test_123",
            type=KnowledgeType.PATTERN,
            title="Test",
            content="Content",
        )

        assert entry.usage_count == 0
        entry.increment_usage()
        assert entry.usage_count == 1
        entry.increment_usage()
        assert entry.usage_count == 2

    def test_entry_to_dict(self):
        """Test serialization to dict."""
        entry = KnowledgeEntry(
            id="test_123",
            type=KnowledgeType.BEST_PRACTICE,
            title="Best Practice",
            content="Always do this",
            tags=["best", "practice"],
            confidence=0.95,
        )

        data = entry.to_dict()

        assert data["id"] == "test_123"
        assert data["type"] == "best_practice"
        assert data["title"] == "Best Practice"
        assert data["confidence"] == 0.95
        assert "created_at" in data

    def test_entry_from_dict(self):
        """Test deserialization from dict."""
        data = {
            "id": "test_456",
            "type": "bug",
            "title": "Bug Fix",
            "content": "Fixed memory leak",
            "tags": ["bug", "memory"],
            "confidence": 0.8,
            "usage_count": 5,
            "created_at": "2026-02-18T10:00:00",
            "updated_at": "2026-02-18T10:00:00",
            "metadata": {},
        }

        entry = KnowledgeEntry.from_dict(data)

        assert entry.id == "test_456"
        assert entry.type == KnowledgeType.BUG
        assert entry.usage_count == 5
        assert entry.confidence == 0.8


# =============================================================================
# SIMPLE VECTOR STORE TESTS
# =============================================================================


class TestSimpleVectorStore:
    """Test SimpleVectorStore implementation."""

    def test_add_and_search(self):
        """Test adding and searching entries."""
        store = SimpleVectorStore()

        store.add("entry1", "React hooks pattern for state management", {"type": "pattern"})
        store.add("entry2", "Python list comprehensions guide", {"type": "lesson"})
        store.add("entry3", "React context API vs Redux", {"type": "pattern"})

        results = store.search("React hooks", top_k=2)

        assert len(results) > 0
        assert any(r["id"] == "entry1" for r in results)

    def test_search_no_match(self):
        """Test search with no matches."""
        store = SimpleVectorStore()
        store.add("entry1", "Python code", {})

        results = store.search("JavaScript React")

        assert len(results) == 0

    def test_delete(self):
        """Test deleting entries."""
        store = SimpleVectorStore()
        store.add("entry1", "Content", {})

        assert store.delete("entry1") is True
        assert store.delete("entry1") is False  # Already deleted

    def test_clear(self):
        """Test clearing store."""
        store = SimpleVectorStore()
        store.add("entry1", "Content", {})
        store.add("entry2", "Content", {})

        store.clear()

        results = store.search("Content")
        assert len(results) == 0


# =============================================================================
# COLLECTIVE KNOWLEDGE BASE TESTS
# =============================================================================


class TestCollectiveKnowledgeBase:
    """Test CollectiveKnowledgeBase."""

    @pytest.fixture
    def ckb(self):
        """Create fresh CKB for each test."""
        return CollectiveKnowledgeBase()

    def test_add_entry(self, ckb):
        """Test adding entry."""
        entry = KnowledgeEntry(
            id="",
            type=KnowledgeType.PATTERN,
            title="Factory Pattern",
            content="Use factory method to create objects",
        )

        added = ckb.add(entry)

        assert added.id != ""
        assert ckb.get(added.id) is not None

    def test_get_entry(self, ckb):
        """Test retrieving entry."""
        entry = KnowledgeEntry(
            id="test_123",
            type=KnowledgeType.LESSON,
            title="Lesson",
            content="Content",
        )
        ckb.add(entry)

        retrieved = ckb.get("test_123")

        assert retrieved is not None
        assert retrieved.title == "Lesson"
        assert retrieved.usage_count == 1  # Incremented on get

    def test_get_nonexistent(self, ckb):
        """Test getting non-existent entry."""
        result = ckb.get("nonexistent")
        assert result is None

    def test_search_entries(self, ckb):
        """Test searching entries."""
        ckb.add(
            KnowledgeEntry(
                id="",
                type=KnowledgeType.PATTERN,
                title="React Hooks",
                content="Use useState for state management in React",
                tags=["react", "frontend"],
            )
        )

        ckb.add(
            KnowledgeEntry(
                id="",
                type=KnowledgeType.LESSON,
                title="Python Tips",
                content="List comprehensions in Python",
                tags=["python", "backend"],
            )
        )

        results = ckb.search("React state", top_k=5)

        assert len(results) > 0
        assert any("React" in e.title for e in results)

    def test_search_with_filters(self, ckb):
        """Test search with type and tag filters."""
        ckb.add(
            KnowledgeEntry(
                id="",
                type=KnowledgeType.PATTERN,
                title="Pattern A",
                content="Content about React",
                tags=["react"],
            )
        )

        ckb.add(
            KnowledgeEntry(
                id="",
                type=KnowledgeType.LESSON,
                title="Lesson B",
                content="Content about React",
                tags=["react"],
            )
        )

        # Filter by type
        results = ckb.search("React", entry_type=KnowledgeType.PATTERN)
        assert len(results) == 1
        assert results[0].type == KnowledgeType.PATTERN

        # Filter by tags
        results = ckb.add(
            KnowledgeEntry(
                id="",
                type=KnowledgeType.PATTERN,
                title="Pattern B",
                content="Content",
                tags=["vue"],
            )
        )

    def test_get_by_type(self, ckb):
        """Test getting entries by type."""
        ckb.add(KnowledgeEntry(id="", type=KnowledgeType.PATTERN, title="P1", content="C1"))
        ckb.add(KnowledgeEntry(id="", type=KnowledgeType.PATTERN, title="P2", content="C2"))
        ckb.add(KnowledgeEntry(id="", type=KnowledgeType.LESSON, title="L1", content="C3"))

        patterns = ckb.get_by_type(KnowledgeType.PATTERN)

        assert len(patterns) == 2
        assert all(e.type == KnowledgeType.PATTERN for e in patterns)

    def test_get_by_project(self, ckb):
        """Test getting entries by project."""
        ckb.add(
            KnowledgeEntry(
                id="", type=KnowledgeType.PATTERN, title="P1", content="C1", project_id="proj_123"
            )
        )
        ckb.add(
            KnowledgeEntry(
                id="", type=KnowledgeType.LESSON, title="L1", content="C2", project_id="proj_123"
            )
        )
        ckb.add(
            KnowledgeEntry(
                id="", type=KnowledgeType.PATTERN, title="P2", content="C3", project_id="proj_456"
            )
        )

        entries = ckb.get_by_project("proj_123")

        assert len(entries) == 2
        assert all(e.project_id == "proj_123" for e in entries)

    def test_get_popular(self, ckb):
        """Test getting most popular entries."""
        entry1 = KnowledgeEntry(id="e1", type=KnowledgeType.PATTERN, title="P1", content="C1")
        entry1.usage_count = 10

        entry2 = KnowledgeEntry(id="e2", type=KnowledgeType.PATTERN, title="P2", content="C2")
        entry2.usage_count = 5

        entry3 = KnowledgeEntry(id="e3", type=KnowledgeType.PATTERN, title="P3", content="C3")
        entry3.usage_count = 20

        ckb.add(entry1)
        ckb.add(entry2)
        ckb.add(entry3)

        popular = ckb.get_popular(limit=2)

        assert len(popular) == 2
        assert popular[0].id == "e3"  # Most used
        assert popular[1].id == "e1"  # Second most

    def test_get_recent(self, ckb):
        """Test getting recent entries."""
        from datetime import timedelta

        entry1 = KnowledgeEntry(id="e1", type=KnowledgeType.PATTERN, title="P1", content="C1")
        entry1.created_at = datetime.now() - timedelta(days=2)

        entry2 = KnowledgeEntry(id="e2", type=KnowledgeType.PATTERN, title="P2", content="C2")
        entry2.created_at = datetime.now() - timedelta(days=1)

        entry3 = KnowledgeEntry(id="e3", type=KnowledgeType.PATTERN, title="P3", content="C3")
        entry3.created_at = datetime.now()

        ckb.add(entry1)
        ckb.add(entry2)
        ckb.add(entry3)

        recent = ckb.get_recent(limit=2)

        assert len(recent) == 2
        assert recent[0].id == "e3"  # Most recent

    def test_delete_entry(self, ckb):
        """Test deleting entry."""
        entry = KnowledgeEntry(id="to_delete", type=KnowledgeType.PATTERN, title="T", content="C")
        ckb.add(entry)

        assert ckb.delete("to_delete") is True
        assert ckb.get("to_delete") is None
        assert ckb.delete("to_delete") is False

    def test_update_entry(self, ckb):
        """Test updating entry."""
        entry = KnowledgeEntry(id="to_update", type=KnowledgeType.PATTERN, title="Old", content="C")
        ckb.add(entry)

        entry.title = "New Title"
        updated = ckb.update(entry)

        assert updated.title == "New Title"
        retrieved = ckb.get("to_update")
        assert retrieved.title == "New Title"

    def test_get_stats(self, ckb):
        """Test statistics."""
        ckb.add(KnowledgeEntry(id="", type=KnowledgeType.PATTERN, title="P", content="C"))
        ckb.add(KnowledgeEntry(id="", type=KnowledgeType.PATTERN, title="P2", content="C2"))
        ckb.add(KnowledgeEntry(id="", type=KnowledgeType.LESSON, title="L", content="C"))

        stats = ckb.get_stats()

        assert stats["total_entries"] == 3
        assert stats["by_type"]["pattern"] == 2
        assert stats["by_type"]["lesson"] == 1

    def test_export_import(self, ckb):
        """Test export and import."""
        entry = KnowledgeEntry(
            id="export_test",
            type=KnowledgeType.PATTERN,
            title="Export Test",
            content="Test content",
            tags=["test"],
        )
        ckb.add(entry)

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            filepath = f.name

        try:
            # Export
            ckb.export(filepath)
            assert os.path.exists(filepath)

            # Clear and import
            ckb.clear()
            assert ckb.get_stats()["total_entries"] == 0

            count = ckb.import_from(filepath)
            assert count == 1
            assert ckb.get("export_test") is not None
        finally:
            os.unlink(filepath)

    def test_clear(self, ckb):
        """Test clearing all entries."""
        ckb.add(KnowledgeEntry(id="", type=KnowledgeType.PATTERN, title="P", content="C"))

        ckb.clear()

        stats = ckb.get_stats()
        assert stats["total_entries"] == 0


# =============================================================================
# CONVENIENCE FUNCTIONS TESTS
# =============================================================================


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_add_knowledge(self):
        """Test add_knowledge function."""
        entry = add_knowledge(
            title="Test Pattern",
            content="Test content",
            entry_type=KnowledgeType.PATTERN,
            tags=["test"],
        )

        assert entry.title == "Test Pattern"
        assert entry.type == KnowledgeType.PATTERN
        assert "test" in entry.tags

    def test_search_knowledge(self):
        """Test search_knowledge function."""
        add_knowledge(
            title="React Pattern",
            content="Use hooks for state",
            entry_type=KnowledgeType.PATTERN,
        )

        results = search_knowledge("React hooks", top_k=5)

        assert len(results) > 0

    def test_get_knowledge_stats(self):
        """Test get_knowledge_stats function."""
        add_knowledge("Title", "Content", KnowledgeType.PATTERN)

        stats = get_knowledge_stats()

        assert "total_entries" in stats
        assert "by_type" in stats


# =============================================================================
# KNOWLEDGE TYPE TESTS
# =============================================================================


class TestKnowledgeTypes:
    """Test knowledge types enum."""

    def test_all_types(self):
        """Test all knowledge types exist."""
        types = list(KnowledgeType)

        assert KnowledgeType.PATTERN in types
        assert KnowledgeType.LESSON in types
        assert KnowledgeType.DECISION in types
        assert KnowledgeType.METRIC in types
        assert KnowledgeType.BUG in types
        assert KnowledgeType.OPTIMIZATION in types
        assert KnowledgeType.BEST_PRACTICE in types

        assert len(types) == 7


# =============================================================================
# INTEGRATION TESTS
# =============================================================================


class TestCKBIntegration:
    """Integration tests for CKB."""

    def test_full_workflow(self):
        """Test complete CKB workflow."""
        ckb = CollectiveKnowledgeBase()

        # Add knowledge
        entry1 = ckb.add(
            KnowledgeEntry(
                id="",
                type=KnowledgeType.PATTERN,
                title="Factory Pattern",
                content="Use factory method for object creation",
                tags=["design-pattern", "creational"],
            )
        )

        entry2 = ckb.add(
            KnowledgeEntry(
                id="",
                type=KnowledgeType.LESSON,
                title="Memory Leak Fix",
                content="Always clean up event listeners",
                tags=["bug", "memory"],
            )
        )

        # Search
        results = ckb.search("factory object creation")
        assert len(results) >= 1

        # Get by type
        patterns = ckb.get_by_type(KnowledgeType.PATTERN)
        assert len(patterns) == 1

        # Update usage
        ckb.get(entry1.id)
        ckb.get(entry1.id)

        # Check stats
        stats = ckb.get_stats()
        assert stats["total_entries"] == 2
        assert stats["total_usage"] >= 2

        # Export/import
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            filepath = f.name

        try:
            ckb.export(filepath)

            ckb2 = CollectiveKnowledgeBase()
            ckb2.import_from(filepath)

            assert ckb2.get_stats()["total_entries"] == 2
        finally:
            os.unlink(filepath)
