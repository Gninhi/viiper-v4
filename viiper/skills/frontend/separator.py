"""Premium Separator Component Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class PremiumSeparatorSkill(Skill):
    """Premium separator/divider for visual separation."""

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Separator Component",
        slug="premium-separator",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.BEGINNER,
        tags=["react", "separator", "divider", "ui", "typescript"],
        estimated_time_minutes=5,
        description="Visual separator with horizontal/vertical orientations",
    )

    dependencies: list = [
        Dependency(name="react", version="^18.0.0", package_manager="npm", reason="UI library"),
        Dependency(name="@radix-ui/react-separator", version="^1.0.3", package_manager="npm", reason="Separator primitives"),
        Dependency(name="tailwindcss", version="^3.4.0", package_manager="npm", reason="Styling"),
    ]

    best_practices: list = [
        BestPractice(title="Use for Visual Grouping", description="Separate related content sections", code_reference="Between menu sections", benefit="Clear content organization"),
    ]

    usage_examples: list = [
        UsageExample(name="Horizontal Divider", description="Separate vertical content", code='<Separator />'),
        UsageExample(name="Vertical Divider", description="Separate horizontal items", code='<Separator orientation="vertical" />'),
    ]

    anti_patterns: list = [
        AntiPattern(bad="Overuse separators", why="Cluttered, hard to scan", good="Use sparingly for major sections"),
    ]

    file_structure: dict = {"components/ui/separator.tsx": "Separator component"}

    component_code: str = '''// components/ui/separator.tsx
import * as React from "react"
import * as SeparatorPrimitive from "@radix-ui/react-separator"

const Separator = React.forwardRef<
  React.ElementRef<typeof SeparatorPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof SeparatorPrimitive.Root>
>(({ className, orientation = "horizontal", decorative = true, ...props }, ref) => (
  <SeparatorPrimitive.Root
    ref={ref}
    decorative={decorative}
    orientation={orientation}
    className={`shrink-0 bg-gray-200 ${
      orientation === "horizontal" ? "h-[1px] w-full" : "h-full w-[1px]"
    } ${className || ""}`}
    {...props}
  />
))
Separator.displayName = SeparatorPrimitive.Root.displayName

export { Separator }
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {"components/ui/separator.tsx": self.component_code}
