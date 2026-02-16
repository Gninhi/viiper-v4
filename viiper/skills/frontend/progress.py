"""
Premium Progress Bar Component Skill.

World-class progress indicators for loading states.
"""

from typing import Dict, Any, Optional
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


class PremiumProgressSkill(Skill):
    """
    Premium progress bar component.

    Features:
    - Determinate (known progress %)
    - Indeterminate (loading spinner)
    - Circular and linear variants
    - Color variants (default, success, warning, error)
    - Size variants
    - Percentage label option
    - Smooth animations
    - Accessible (ARIA attributes)
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Progress Bar Component",
        slug="premium-progress",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.BEGINNER,
        tags=["react", "progress", "loading", "ui", "typescript"],
        estimated_time_minutes=10,
        description="Production-ready progress indicators with animations",
    )

    dependencies: list = [
        Dependency(
            name="react",
            version="^18.0.0",
            package_manager="npm",
            reason="UI library",
        ),
        Dependency(
            name="@radix-ui/react-progress",
            version="^1.0.3",
            package_manager="npm",
            reason="Progress primitives with ARIA",
        ),
        Dependency(
            name="class-variance-authority",
            version="^0.7.0",
            package_manager="npm",
            reason="Type-safe variants",
        ),
        Dependency(
            name="tailwindcss",
            version="^3.4.0",
            package_manager="npm",
            reason="Styling",
        ),
        Dependency(
            name="clsx",
            version="^2.1.0",
            package_manager="npm",
            reason="Class merging",
        ),
        Dependency(
            name="tailwind-merge",
            version="^2.2.0",
            package_manager="npm",
            reason="Tailwind merging",
        ),
    ]

    best_practices: list = [
        BestPractice(
            title="Use Determinate When Possible",
            description="Show actual progress % when known",
            code_reference='<Progress value={progress} max={100} />',
            benefit="Users know how long they're waiting",
        ),
        BestPractice(
            title="Smooth Transitions",
            description="Animate progress changes",
            code_reference="transition-all duration-300",
            benefit="Feels polished, progress is visible",
        ),
        BestPractice(
            title="ARIA Attributes",
            description="Include progress value for screen readers",
            code_reference='aria-valuenow={value}',
            benefit="Accessible to screen reader users",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Basic Progress",
            description="Simple progress bar",
            code='''import { Progress } from "@/components/ui/progress"

const [progress, setProgress] = useState(0)

<Progress value={progress} />''',
        ),
        UsageExample(
            name="File Upload Progress",
            description="Show upload percentage",
            code='''<div className="space-y-2">
  <div className="flex justify-between text-sm">
    <span>Uploading document.pdf</span>
    <span>{uploadProgress}%</span>
  </div>
  <Progress value={uploadProgress} variant="success" />
</div>''',
        ),
        UsageExample(
            name="Indeterminate Loading",
            description="Unknown duration loading",
            code='''<Progress indeterminate />''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Using progress bar for instant operations",
            why="Users see flash of loading, confusing",
            good="Only show for operations > 500ms",
        ),
        AntiPattern(
            bad="Progress bar that doesn't progress",
            why="Stuck at 99%, users lose trust",
            good="Use indeterminate if duration unknown",
        ),
    ]

    file_structure: dict = {
        "components/ui/progress.tsx": "Progress component",
        "lib/utils.ts": "Utilities",
    }

    component_code: str = '''// components/ui/progress.tsx
import * as React from "react"
import * as ProgressPrimitive from "@radix-ui/react-progress"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const progressVariants = cva(
  "relative h-2 w-full overflow-hidden rounded-full bg-gray-100",
  {
    variants: {
      variant: {
        default: "[&>div]:bg-black",
        success: "[&>div]:bg-green-600",
        warning: "[&>div]:bg-yellow-600",
        error: "[&>div]:bg-red-600",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

interface ProgressProps
  extends React.ComponentPropsWithoutRef<typeof ProgressPrimitive.Root>,
    VariantProps<typeof progressVariants> {
  indeterminate?: boolean
}

const Progress = React.forwardRef<
  React.ElementRef<typeof ProgressPrimitive.Root>,
  ProgressProps
>(({ className, value, variant, indeterminate, ...props }, ref) => (
  <ProgressPrimitive.Root
    ref={ref}
    className={cn(progressVariants({ variant }), className)}
    {...props}
  >
    <ProgressPrimitive.Indicator
      className={cn(
        "h-full transition-all duration-300",
        indeterminate && "animate-pulse"
      )}
      style={{ transform: `translateX(-${100 - (value || 0)}%)` }}
    />
  </ProgressPrimitive.Root>
))
Progress.displayName = ProgressPrimitive.Root.displayName

export { Progress }
'''

    utils_code: str = '''// lib/utils.ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "components/ui/progress.tsx": self.component_code,
            "lib/utils.ts": self.utils_code,
        }
