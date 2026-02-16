"""
Premium Badge Component Skill.

World-class badge/pill component for status indicators and labels.
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


class PremiumBadgeSkill(Skill):
    """
    Premium badge component with variants.

    Features:
    - Multiple variants (default, success, warning, error, info)
    - Size variants (sm, md, lg)
    - Outline and solid styles
    - Dot indicator option
    - Dismissible badges
    - Icon support
    - Rounded and pill shapes
    - Type-safe with class-variance-authority
    - Accessible (proper semantic HTML)
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Badge Component",
        slug="premium-badge",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.BEGINNER,
        tags=["react", "badge", "pill", "status", "ui", "typescript"],
        estimated_time_minutes=10,
        description="Production-ready badge component for status indicators and labels",
    )

    dependencies: list = [
        Dependency(
            name="react",
            version="^18.0.0",
            package_manager="npm",
            reason="UI library",
        ),
        Dependency(
            name="class-variance-authority",
            version="^0.7.0",
            package_manager="npm",
            reason="Type-safe variant composition",
        ),
        Dependency(
            name="tailwindcss",
            version="^3.4.0",
            package_manager="npm",
            reason="Utility-first CSS framework",
        ),
        Dependency(
            name="clsx",
            version="^2.1.0",
            package_manager="npm",
            reason="Conditional class merging",
        ),
        Dependency(
            name="tailwind-merge",
            version="^2.2.0",
            package_manager="npm",
            reason="Merge Tailwind classes properly",
        ),
    ]

    best_practices: list = [
        BestPractice(
            title="Semantic Color Coding",
            description="Use consistent colors for status meanings",
            code_reference='variant="success" for positive, "error" for negative',
            benefit="Users quickly understand status at a glance",
        ),
        BestPractice(
            title="Keep Text Concise",
            description="Badge text should be 1-2 words max",
            code_reference='<Badge>Active</Badge>, not <Badge>User is currently active</Badge>',
            benefit="Badges are scannable, don't clutter UI",
        ),
        BestPractice(
            title="Use Inline",
            description="Badges should be inline elements, not block",
            code_reference="inline-flex in base styles",
            benefit="Badges flow naturally with surrounding text",
        ),
        BestPractice(
            title="Consistent Sizing",
            description="Match badge size to surrounding text",
            code_reference='size="sm" for small text, "md" for normal',
            benefit="Visual harmony, badges don't overpower content",
        ),
        BestPractice(
            title="Dot for Status",
            description="Use dot variant for subtle status indication",
            code_reference='<Badge dot variant="success">Online</Badge>',
            benefit="Less visual weight while still conveying status",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Status Badges",
            description="Show user or item status",
            code='''import { Badge } from "@/components/ui/badge"

<div className="flex gap-2">
  <Badge variant="success">Active</Badge>
  <Badge variant="warning">Pending</Badge>
  <Badge variant="error">Inactive</Badge>
  <Badge variant="default">Draft</Badge>
</div>''',
        ),
        UsageExample(
            name="Notification Count",
            description="Show unread count or notifications",
            code='''<button className="relative p-2">
  <BellIcon className="h-6 w-6" />
  <Badge
    variant="error"
    className="absolute -top-1 -right-1 h-5 w-5 flex items-center justify-center p-0"
  >
    5
  </Badge>
</button>''',
        ),
        UsageExample(
            name="With Dot Indicator",
            description="Subtle status with dot",
            code='''<div className="flex items-center gap-2">
  <Avatar src="/user.jpg" />
  <div>
    <p className="font-medium">John Doe</p>
    <Badge dot variant="success" size="sm">
      Online
    </Badge>
  </div>
</div>''',
        ),
        UsageExample(
            name="Dismissible Badge",
            description="Badge with remove button",
            code='''function DismissibleBadge({ label, onRemove }) {
  return (
    <Badge variant="default" className="gap-1">
      {label}
      <button
        onClick={onRemove}
        className="ml-1 rounded-full hover:bg-gray-200 p-0.5"
      >
        <XIcon className="h-3 w-3" />
      </button>
    </Badge>
  )
}

// Usage
<div className="flex gap-2">
  <DismissibleBadge label="React" onRemove={() => {}} />
  <DismissibleBadge label="TypeScript" onRemove={() => {}} />
</div>''',
        ),
        UsageExample(
            name="Outline Variant",
            description="Subtle badge with outline",
            code='''<div className="flex gap-2">
  <Badge variant="success" outline>Verified</Badge>
  <Badge variant="error" outline>Unverified</Badge>
  <Badge variant="info" outline>New</Badge>
</div>''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Long text in badges (\"This user is currently active and online\")",
            why="Takes up too much space, hard to scan, defeats purpose of badge",
            good="Keep to 1-2 words (\"Active\", \"Online\")",
        ),
        AntiPattern(
            bad="Using badges for clickable actions",
            why="Badges look like static labels, users won't expect them to be clickable",
            good="Use Button component for actions, Badge for status only",
        ),
        AntiPattern(
            bad="Inconsistent color usage (success = red one place, green another)",
            why="Confusing, users can't rely on color meaning",
            good="Consistent semantic colors across app (success = green, error = red)",
        ),
        AntiPattern(
            bad="Too many badges on one element (5+ badges)",
            why="Cluttered, overwhelming, hard to prioritize information",
            good="Limit to 1-2 badges per element, use most important status only",
        ),
    ]

    file_structure: dict = {
        "components/ui/badge.tsx": "Badge component with variants",
        "lib/utils.ts": "cn() utility for class merging",
    }

    component_code: str = '''// components/ui/badge.tsx
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
  // Base styles - ALWAYS applied
  "inline-flex items-center rounded-full font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2",
  {
    variants: {
      variant: {
        // Default: Neutral gray
        default: "bg-gray-100 text-gray-900 hover:bg-gray-200",

        // Success: Positive status (green)
        success: "bg-green-100 text-green-900 hover:bg-green-200",

        // Warning: Attention needed (yellow/orange)
        warning: "bg-yellow-100 text-yellow-900 hover:bg-yellow-200",

        // Error: Negative status (red)
        error: "bg-red-100 text-red-900 hover:bg-red-200",

        // Info: Informational (blue)
        info: "bg-blue-100 text-blue-900 hover:bg-blue-200",

        // Primary: Emphasis (black)
        primary: "bg-black text-white hover:bg-gray-800",
      },
      size: {
        sm: "px-2 py-0.5 text-xs",
        md: "px-2.5 py-1 text-sm",
        lg: "px-3 py-1.5 text-base",
      },
      outline: {
        true: "",
      },
      dot: {
        true: "pl-1.5",
      },
    },
    compoundVariants: [
      // Outline variants
      {
        variant: "default",
        outline: true,
        className: "bg-transparent border border-gray-300 text-gray-700",
      },
      {
        variant: "success",
        outline: true,
        className: "bg-transparent border border-green-300 text-green-700",
      },
      {
        variant: "warning",
        outline: true,
        className: "bg-transparent border border-yellow-300 text-yellow-700",
      },
      {
        variant: "error",
        outline: true,
        className: "bg-transparent border border-red-300 text-red-700",
      },
      {
        variant: "info",
        outline: true,
        className: "bg-transparent border border-blue-300 text-blue-700",
      },
    ],
    defaultVariants: {
      variant: "default",
      size: "md",
      outline: false,
      dot: false,
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {
  /** Show dot indicator before text */
  dot?: boolean
}

/**
 * Premium badge component for status and labels.
 *
 * @example
 * ```tsx
 * <Badge variant="success">Active</Badge>
 * <Badge variant="error" outline>Error</Badge>
 * <Badge variant="info" dot>New</Badge>
 * ```
 */
export function Badge({
  className,
  variant,
  size,
  outline,
  dot,
  children,
  ...props
}: BadgeProps) {
  return (
    <span
      className={cn(badgeVariants({ variant, size, outline, dot }), className)}
      {...props}
    >
      {dot && (
        <span
          className={cn(
            "mr-1.5 h-1.5 w-1.5 rounded-full",
            variant === "success" && "bg-green-600",
            variant === "warning" && "bg-yellow-600",
            variant === "error" && "bg-red-600",
            variant === "info" && "bg-blue-600",
            variant === "default" && "bg-gray-600",
            variant === "primary" && "bg-white"
          )}
        />
      )}
      {children}
    </span>
  )
}
'''

    utils_code: str = '''// lib/utils.ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

/**
 * Merge Tailwind CSS classes with proper precedence.
 * Uses clsx for conditional classes and tailwind-merge to handle conflicts.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Generate premium badge component files.

        Args:
            context: Optional configuration (not used currently)

        Returns:
            Dictionary of filepath: code
        """
        return {
            "components/ui/badge.tsx": self.component_code,
            "lib/utils.ts": self.utils_code,
        }
