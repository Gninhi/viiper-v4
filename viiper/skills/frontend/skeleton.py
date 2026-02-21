"""Premium Skeleton Component Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)
from viiper.skills.common_dependencies import FRONTEND_BASE_DEPS

class PremiumSkeletonSkill(Skill):
    """Premium skeleton loading placeholders."""

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Skeleton Component",
        slug="premium-skeleton",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.BEGINNER,
        tags=["react", "skeleton", "loading", "ui", "typescript"],
        estimated_time_minutes=5,
        description="Loading placeholders for better perceived performance",
    )

    dependencies: list = FRONTEND_BASE_DEPS

    best_practices: list = [
        BestPractice(title="Match Content Shape", description="Skeleton should match final content layout", code_reference="Same heights/widths", benefit="Smooth transition when loaded"),
    ]

    usage_examples: list = [
        UsageExample(name="Card Skeleton", description="Loading card placeholder", code='<Skeleton className="h-32 w-full" />'),
    ]

    anti_patterns: list = [
        AntiPattern(bad="Generic rectangles", why="Doesn't match content", good="Match final layout shape"),
    ]

    file_structure: dict = {"components/ui/skeleton.tsx": "Skeleton component"}

    component_code: str = '''// components/ui/skeleton.tsx
import * as React from "react"

interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {}

function Skeleton({ className, ...props }: SkeletonProps) {
  return (
    <div
      className={`animate-pulse rounded-md bg-gray-200 ${className || ""}`}
      {...props}
    />
  )
}

export { Skeleton }
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {"components/ui/skeleton.tsx": self.component_code}
