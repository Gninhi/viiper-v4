"""
Skill Registry for managing and searching skills.

Central registry of all available skills in VIIPER.
"""

from typing import Dict, List, Optional, Type
from viiper.skills.base import Skill, SkillCategory, SkillDifficulty


class SkillRegistry:
    """
    Central registry for all skills.

    Provides:
    - Skill registration
    - Search and filtering
    - Skill retrieval
    """

    # Class variable: registry of all skills
    _skills: Dict[str, Type[Skill]] = {}

    # Indexes for fast lookup
    _by_category: Dict[SkillCategory, List[str]] = {}
    _by_tag: Dict[str, List[str]] = {}
    _by_difficulty: Dict[SkillDifficulty, List[str]] = {}

    @classmethod
    def register(cls, skill_class: Type[Skill]) -> None:
        """
        Register a skill class.

        Args:
            skill_class: Skill class to register

        Example:
            SkillRegistry.register(PremiumButtonSkill)
        """
        # Instantiate to get metadata
        skill = skill_class()

        slug = skill.metadata.slug

        # Register in main registry
        cls._skills[slug] = skill_class

        # Index by category
        category = skill.metadata.category
        if category not in cls._by_category:
            cls._by_category[category] = []
        cls._by_category[category].append(slug)

        # Index by difficulty
        difficulty = skill.metadata.difficulty
        if difficulty not in cls._by_difficulty:
            cls._by_difficulty[difficulty] = []
        cls._by_difficulty[difficulty].append(slug)

        # Index by tags
        for tag in skill.metadata.tags:
            tag_lower = tag.lower()
            if tag_lower not in cls._by_tag:
                cls._by_tag[tag_lower] = []
            cls._by_tag[tag_lower].append(slug)

    @classmethod
    def get(cls, slug: str) -> Optional[Skill]:
        """
        Get skill instance by slug.

        Args:
            slug: Skill slug

        Returns:
            Skill instance or None if not found
        """
        skill_class = cls._skills.get(slug)
        if skill_class:
            return skill_class()
        return None

    @classmethod
    def get_class(cls, slug: str) -> Optional[Type[Skill]]:
        """
        Get skill class by slug.

        Args:
            slug: Skill slug

        Returns:
            Skill class or None if not found
        """
        return cls._skills.get(slug)

    @classmethod
    def list_all(cls) -> List[str]:
        """
        List all registered skill slugs.

        Returns:
            List of skill slugs
        """
        return list(cls._skills.keys())

    @classmethod
    def list_all_skills(cls) -> List[Skill]:
        """
        List all registered skills as instances.

        Returns:
            List of Skill instances
        """
        return [skill_class() for skill_class in cls._skills.values()]

    @classmethod
    def search(
        cls,
        category: Optional[SkillCategory] = None,
        difficulty: Optional[SkillDifficulty] = None,
        tags: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None,
    ) -> List[Skill]:
        """
        Search skills by various criteria.

        Args:
            category: Filter by category
            difficulty: Filter by difficulty
            tags: Filter by tags (OR logic - any tag matches)
            keywords: Search in name/description (OR logic)

        Returns:
            List of matching Skill instances

        Example:
            # Find frontend components for beginners
            skills = SkillRegistry.search(
                category=SkillCategory.FRONTEND_COMPONENTS,
                difficulty=SkillDifficulty.BEGINNER
            )

            # Find skills with specific tags
            skills = SkillRegistry.search(
                tags=["react", "typescript"]
            )
        """
        candidates = set(cls._skills.keys())

        # Filter by category
        if category is not None:
            category_skills = set(cls._by_category.get(category, []))
            candidates = candidates.intersection(category_skills)

        # Filter by difficulty
        if difficulty is not None:
            difficulty_skills = set(cls._by_difficulty.get(difficulty, []))
            candidates = candidates.intersection(difficulty_skills)

        # Filter by tags (OR logic - any tag matches)
        if tags:
            tag_skills = set()
            for tag in tags:
                tag_lower = tag.lower()
                tag_skills.update(cls._by_tag.get(tag_lower, []))
            candidates = candidates.intersection(tag_skills)

        # Filter by keywords (search in name/description)
        if keywords:
            keyword_skills = set()
            for slug in candidates:
                skill = cls.get(slug)
                if skill:
                    text = (
                        skill.metadata.name.lower()
                        + " "
                        + skill.metadata.description.lower()
                    )
                    if any(kw.lower() in text for kw in keywords):
                        keyword_skills.add(slug)
            candidates = candidates.intersection(keyword_skills)

        # Return skill instances
        return [cls.get(slug) for slug in candidates if cls.get(slug)]

    @classmethod
    def get_by_category(cls, category: SkillCategory) -> List[Skill]:
        """
        Get all skills in a category.

        Args:
            category: Skill category

        Returns:
            List of Skill instances
        """
        slugs = cls._by_category.get(category, [])
        return [cls.get(slug) for slug in slugs if cls.get(slug)]

    @classmethod
    def get_by_difficulty(cls, difficulty: SkillDifficulty) -> List[Skill]:
        """
        Get all skills at a difficulty level.

        Args:
            difficulty: Skill difficulty

        Returns:
            List of Skill instances
        """
        slugs = cls._by_difficulty.get(difficulty, [])
        return [cls.get(slug) for slug in slugs if cls.get(slug)]

    @classmethod
    def get_by_tags(cls, tags: List[str]) -> List[Skill]:
        """
        Get skills matching any of the given tags.

        Args:
            tags: List of tags

        Returns:
            List of Skill instances
        """
        slug_set = set()
        for tag in tags:
            tag_lower = tag.lower()
            slug_set.update(cls._by_tag.get(tag_lower, []))

        return [cls.get(slug) for slug in slug_set if cls.get(slug)]

    @classmethod
    def get_statistics(cls) -> Dict:
        """
        Get registry statistics.

        Returns:
            Dictionary with statistics
        """
        return {
            "total_skills": len(cls._skills),
            "by_category": {
                cat.value: len(slugs) for cat, slugs in cls._by_category.items()
            },
            "by_difficulty": {
                diff.value: len(slugs) for diff, slugs in cls._by_difficulty.items()
            },
            "total_tags": len(cls._by_tag),
        }

    @classmethod
    def clear(cls) -> None:
        """Clear the registry (useful for testing)."""
        cls._skills.clear()
        cls._by_category.clear()
        cls._by_tag.clear()
        cls._by_difficulty.clear()

    @classmethod
    def generate_catalog(cls) -> str:
        """
        Generate markdown catalog of all skills.

        Returns:
            Markdown string
        """
        md = "# Skills Catalog\n\n"

        stats = cls.get_statistics()
        md += f"**Total Skills**: {stats['total_skills']}\n\n"

        # Group by category
        for category in SkillCategory:
            skills = cls.get_by_category(category)
            if not skills:
                continue

            md += f"## {category.value.replace('_', ' ').title()}\n\n"
            md += f"*{len(skills)} skills*\n\n"

            for skill in sorted(skills, key=lambda s: s.metadata.name):
                md += f"### {skill.metadata.name}\n\n"
                md += f"**Slug**: `{skill.metadata.slug}`  \n"
                md += f"**Difficulty**: {skill.metadata.difficulty.value}  \n"
                md += f"**Time**: ~{skill.metadata.estimated_time_minutes} min  \n"

                if skill.metadata.tags:
                    md += f"**Tags**: {', '.join(skill.metadata.tags)}  \n"

                if skill.metadata.description:
                    md += f"\n{skill.metadata.description}\n"

                md += "\n---\n\n"

        return md
