"""Premium Label Component Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)
from viiper.skills.common_dependencies import FRONTEND_BASE_DEPS

class PremiumLabelSkill(Skill):
    """Premium label for form inputs."""

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Label Component",
        slug="premium-label",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.BEGINNER,
        tags=["react", "label", "form", "ui", "typescript"],
        estimated_time_minutes=5,
        description="Accessible form labels with proper associations",
    )

    dependencies: list = FRONTEND_BASE_DEPS + [
        Dependency(name="@radix-ui/react-label", version="^2.0.2", package_manager="npm", reason="Label primitives"),
    ]

    best_practices: list = [
        BestPractice(title="Always Use htmlFor", description="Associate label with input", code_reference='<Label htmlFor="input-id">', benefit="Click label to focus input"),
    ]

    usage_examples: list = [
        UsageExample(name="Form Label", description="Label for input field", code='<Label htmlFor="email">Email</Label>\n<Input id="email" />'),
    ]

    anti_patterns: list = [
        AntiPattern(bad="Label without htmlFor", why="Not associated with input", good="Always use htmlFor attribute"),
    ]

    file_structure: dict = {"components/ui/label.tsx": "Label component"}

    component_code: str = '''// components/ui/label.tsx
import * as React from "react"
import * as LabelPrimitive from "@radix-ui/react-label"

const Label = React.forwardRef<
  React.ElementRef<typeof LabelPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof LabelPrimitive.Root>
>(({ className, ...props }, ref) => (
  <LabelPrimitive.Root
    ref={ref}
    className={`text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 ${className || ""}`}
    {...props}
  />
))
Label.displayName = LabelPrimitive.Root.displayName

export { Label }
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {"components/ui/label.tsx": self.component_code}
