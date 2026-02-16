"""
Unit tests for Skills Library infrastructure.

Tests base classes, registry, and loader.
"""

import pytest
from viiper.skills.base import (
    Skill,
    SkillMetadata,
    SkillCategory,
    SkillDifficulty,
    Dependency,
    BestPractice,
    UsageExample,
    AntiPattern,
)
from viiper.skills.registry import SkillRegistry
from viiper.skills.loader import SkillLoader
from typing import Dict, Any, Optional


# Test Skill for testing
class TestButtonSkill(Skill):
    """Test button skill."""

    metadata: SkillMetadata = SkillMetadata(
        name="Test Button",
        slug="test-button",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.BEGINNER,
        tags=["react", "button", "test"],
        description="A test button component",
    )

    dependencies: list = [
        Dependency(name="react", version="^18.0.0", package_manager="npm")
    ]

    best_practices: list = [
        BestPractice(
            title="Use Semantic HTML",
            description="Always use <button> element",
            code_reference="<button>Click</button>",
        )
    ]

    usage_examples: list = [
        UsageExample(
            name="Basic",
            description="Basic button usage",
            code='<Button>Click me</Button>',
        )
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Using div as button",
            why="Not accessible",
            good="Use button element",
        )
    ]

    file_structure: dict = {"button.tsx": "Button component"}

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {"button.tsx": "const Button = () => <button>Click</button>"}


class TestAdvancedSkill(Skill):
    """Test advanced skill."""

    metadata: SkillMetadata = SkillMetadata(
        name="Advanced Skill",
        slug="advanced-skill",
        category=SkillCategory.BACKEND_AUTH,
        difficulty=SkillDifficulty.ADVANCED,
        tags=["auth", "security"],
    )

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {"auth.ts": "// Auth code"}


class TestSkillMetadata:
    """Test SkillMetadata model."""

    def test_metadata_creation(self):
        """Test creating metadata."""
        metadata = SkillMetadata(
            name="Test Skill",
            slug="test-skill",
            category=SkillCategory.FRONTEND_COMPONENTS,
        )

        assert metadata.name == "Test Skill"
        assert metadata.slug == "test-skill"
        assert metadata.category == SkillCategory.FRONTEND_COMPONENTS
        assert metadata.version == "1.0.0"  # default
        assert metadata.difficulty == SkillDifficulty.INTERMEDIATE  # default

    def test_metadata_with_tags(self):
        """Test metadata with tags."""
        metadata = SkillMetadata(
            name="Tagged Skill",
            slug="tagged",
            category=SkillCategory.BACKEND_API,
            tags=["api", "rest", "express"],
        )

        assert "api" in metadata.tags
        assert len(metadata.tags) == 3


class TestDependency:
    """Test Dependency model."""

    def test_dependency_creation(self):
        """Test creating dependency."""
        dep = Dependency(
            name="react", version="^18.0.0", package_manager="npm", reason="UI library"
        )

        assert dep.name == "react"
        assert dep.version == "^18.0.0"
        assert dep.package_manager == "npm"
        assert dep.reason == "UI library"


class TestSkillBase:
    """Test Skill base class."""

    def test_skill_creation(self):
        """Test creating a skill."""
        skill = TestButtonSkill()

        assert skill.metadata.name == "Test Button"
        assert skill.metadata.slug == "test-button"
        assert len(skill.dependencies) == 1
        assert len(skill.best_practices) == 1

    def test_skill_generate(self):
        """Test skill generate method."""
        skill = TestButtonSkill()
        code = skill.generate()

        assert "button.tsx" in code
        assert "Button" in code["button.tsx"]

    def test_get_installation_steps(self):
        """Test installation steps generation."""
        skill = TestButtonSkill()
        steps = skill.get_installation_steps()

        assert len(steps) > 0
        assert any("npm install" in step for step in steps)
        assert any("button.tsx" in step for step in steps)

    def test_get_documentation(self):
        """Test documentation generation."""
        skill = TestButtonSkill()
        doc = skill.get_documentation()

        assert "Test Button" in doc
        assert "Dependencies" in doc
        assert "Best Practices" in doc
        assert "Usage Examples" in doc
        assert "Anti-Patterns" in doc


class TestSkillRegistry:
    """Test SkillRegistry."""

    def setup_method(self):
        """Clear registry before each test."""
        SkillRegistry.clear()

    def test_register_skill(self):
        """Test registering a skill."""
        SkillRegistry.register(TestButtonSkill)

        assert "test-button" in SkillRegistry.list_all()

    def test_get_skill(self):
        """Test retrieving a skill."""
        SkillRegistry.register(TestButtonSkill)

        skill = SkillRegistry.get("test-button")
        assert skill is not None
        assert skill.metadata.name == "Test Button"

    def test_get_nonexistent_skill(self):
        """Test getting nonexistent skill."""
        skill = SkillRegistry.get("nonexistent")
        assert skill is None

    def test_search_by_category(self):
        """Test searching by category."""
        SkillRegistry.register(TestButtonSkill)
        SkillRegistry.register(TestAdvancedSkill)

        frontend = SkillRegistry.search(category=SkillCategory.FRONTEND_COMPONENTS)
        assert len(frontend) == 1
        assert frontend[0].metadata.slug == "test-button"

        backend = SkillRegistry.search(category=SkillCategory.BACKEND_AUTH)
        assert len(backend) == 1

    def test_search_by_difficulty(self):
        """Test searching by difficulty."""
        SkillRegistry.register(TestButtonSkill)
        SkillRegistry.register(TestAdvancedSkill)

        beginner = SkillRegistry.search(difficulty=SkillDifficulty.BEGINNER)
        assert len(beginner) == 1

        advanced = SkillRegistry.search(difficulty=SkillDifficulty.ADVANCED)
        assert len(advanced) == 1

    def test_search_by_tags(self):
        """Test searching by tags."""
        SkillRegistry.register(TestButtonSkill)
        SkillRegistry.register(TestAdvancedSkill)

        react_skills = SkillRegistry.search(tags=["react"])
        assert len(react_skills) == 1
        assert react_skills[0].metadata.slug == "test-button"

    def test_search_by_keywords(self):
        """Test searching by keywords."""
        SkillRegistry.register(TestButtonSkill)

        skills = SkillRegistry.search(keywords=["button"])
        assert len(skills) == 1

    def test_get_by_category(self):
        """Test getting skills by category."""
        SkillRegistry.register(TestButtonSkill)

        skills = SkillRegistry.get_by_category(SkillCategory.FRONTEND_COMPONENTS)
        assert len(skills) == 1

    def test_get_statistics(self):
        """Test registry statistics."""
        SkillRegistry.register(TestButtonSkill)
        SkillRegistry.register(TestAdvancedSkill)

        stats = SkillRegistry.get_statistics()
        assert stats["total_skills"] == 2
        assert stats["by_category"][SkillCategory.FRONTEND_COMPONENTS.value] == 1
        assert stats["by_difficulty"][SkillDifficulty.BEGINNER.value] == 1

    def test_generate_catalog(self):
        """Test catalog generation."""
        SkillRegistry.register(TestButtonSkill)

        catalog = SkillRegistry.generate_catalog()
        assert "Skills Catalog" in catalog
        assert "Test Button" in catalog


class TestSkillLoader:
    """Test SkillLoader."""

    def setup_method(self):
        """Clear registry before each test."""
        SkillRegistry.clear()

    def test_validate_skill_valid(self):
        """Test validating a valid skill."""
        errors = SkillLoader.validate_skill(TestButtonSkill)
        assert len(errors) == 0

    def test_validate_skill_invalid_slug(self):
        """Test validating skill with invalid slug."""

        class InvalidSlugSkill(Skill):
            metadata: SkillMetadata = SkillMetadata(
                name="Invalid",
                slug="Invalid_Slug",  # Should be kebab-case
                category=SkillCategory.FRONTEND_COMPONENTS,
            )

            def generate(self, context=None):
                return {}

        errors = SkillLoader.validate_skill(InvalidSlugSkill)
        assert any("kebab-case" in err.lower() for err in errors)

    def test_reload_all(self):
        """Test reloading all skills."""
        # Register a skill
        SkillRegistry.register(TestButtonSkill)
        assert len(SkillRegistry.list_all()) == 1

        # Reload clears and reloads from packages
        # (should find 0 since we don't have skills in packages yet)
        count = SkillLoader.reload_all()
        # Count may be 0 since packages are empty
        assert isinstance(count, int)


# Run with: pytest tests/unit/test_skills.py -v
