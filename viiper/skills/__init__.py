"""
VIIPER Skills Library.

Production-ready code templates that agents use to generate high-quality code.
"""

from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty
from viiper.skills.registry import SkillRegistry
from viiper.skills.loader import SkillLoader

__all__ = [
    "Skill",
    "SkillMetadata",
    "SkillCategory",
    "SkillDifficulty",
    "SkillRegistry",
    "SkillLoader",
]
