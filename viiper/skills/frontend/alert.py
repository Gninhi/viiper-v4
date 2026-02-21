"""Premium Alert Component Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)
from viiper.skills.common_dependencies import FRONTEND_BASE_DEPS

class PremiumAlertSkill(Skill):
    """Premium alert/callout for important messages."""

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Alert Component",
        slug="premium-alert",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.BEGINNER,
        tags=["react", "alert", "notification", "ui", "typescript"],
        estimated_time_minutes=10,
        description="Alert banners for success, error, warning, and info messages",
    )

    dependencies: list = FRONTEND_BASE_DEPS

    best_practices: list = [
        BestPractice(title="Use Semantic Variants", description="Match variant to message type", code_reference='variant="error" for errors', benefit="Clear visual communication"),
    ]

    usage_examples: list = [
        UsageExample(name="Success Alert", description="Show success message", code='<Alert variant="success">\n  <Alert.Title>Success!</Alert.Title>\n  <Alert.Description>Changes saved</Alert.Description>\n</Alert>'),
        UsageExample(name="Error Alert", description="Show error message", code='<Alert variant="error">\n  <Alert.Title>Error</Alert.Title>\n  <Alert.Description>Failed to save</Alert.Description>\n</Alert>'),
    ]

    anti_patterns: list = [
        AntiPattern(bad="Using alerts for every action", why="Alert fatigue", good="Reserve for important messages"),
    ]

    file_structure: dict = {"components/ui/alert.tsx": "Alert component"}

    component_code: str = '''// components/ui/alert.tsx
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"

const alertVariants = cva(
  "relative w-full rounded-lg border p-4",
  {
    variants: {
      variant: {
        default: "bg-white border-gray-200",
        success: "bg-green-50 border-green-200 text-green-900",
        error: "bg-red-50 border-red-200 text-red-900",
        warning: "bg-yellow-50 border-yellow-200 text-yellow-900",
        info: "bg-blue-50 border-blue-200 text-blue-900",
      },
    },
    defaultVariants: { variant: "default" },
  }
)

interface AlertProps extends React.HTMLAttributes<HTMLDivElement>, VariantProps<typeof alertVariants> {}

const Alert = React.forwardRef<HTMLDivElement, AlertProps>(
  ({ className, variant, ...props }, ref) => (
    <div ref={ref} role="alert" className={`${alertVariants({ variant })} ${className || ""}`} {...props} />
  )
)
Alert.displayName = "Alert"

const AlertTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h5 ref={ref} className={`mb-1 font-medium leading-none tracking-tight ${className || ""}`} {...props} />
  )
)
AlertTitle.displayName = "AlertTitle"

const AlertDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={`text-sm [&_p]:leading-relaxed ${className || ""}`} {...props} />
  )
)
AlertDescription.displayName = "AlertDescription"

export { Alert, AlertTitle, AlertDescription }
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {"components/ui/alert.tsx": self.component_code}
