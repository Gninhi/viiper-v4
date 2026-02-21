"""Premium Slider Component Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)
from viiper.skills.common_dependencies import FRONTEND_BASE_DEPS

class PremiumSliderSkill(Skill):
    """Premium slider for range inputs."""

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Slider Component",
        slug="premium-slider",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.BEGINNER,
        tags=["react", "slider", "range", "ui", "typescript"],
        estimated_time_minutes=10,
        description="Range slider with Radix UI",
    )

    dependencies: list = FRONTEND_BASE_DEPS + [
        Dependency(name="@radix-ui/react-slider", version="^1.1.2", package_manager="npm", reason="Slider primitives"),
    ]

    best_practices: list = [
        BestPractice(title="Show Current Value", description="Display value label", code_reference="<span>{value}</span>", benefit="Users see selected value"),
    ]

    usage_examples: list = [
        UsageExample(name="Basic Slider", description="Simple range slider", code='<Slider value={[50]} onValueChange={setValue} />'),
    ]

    anti_patterns: list = [
        AntiPattern(bad="No value display", why="Users don't know selected value", good="Show current value label"),
    ]

    file_structure: dict = {"components/ui/slider.tsx": "Slider component"}

    component_code: str = '''// components/ui/slider.tsx
import * as React from "react"
import * as SliderPrimitive from "@radix-ui/react-slider"

const Slider = React.forwardRef<
  React.ElementRef<typeof SliderPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof SliderPrimitive.Root>
>(({ className, ...props }, ref) => (
  <SliderPrimitive.Root
    ref={ref}
    className="relative flex w-full touch-none select-none items-center"
    {...props}
  >
    <SliderPrimitive.Track className="relative h-2 w-full grow overflow-hidden rounded-full bg-gray-200">
      <SliderPrimitive.Range className="absolute h-full bg-black" />
    </SliderPrimitive.Track>
    <SliderPrimitive.Thumb className="block h-5 w-5 rounded-full border-2 border-black bg-white ring-offset-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50" />
  </SliderPrimitive.Root>
))
Slider.displayName = SliderPrimitive.Root.displayName

export { Slider }
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {"components/ui/slider.tsx": self.component_code}
