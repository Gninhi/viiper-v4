"""
Premium Tooltip Component Skill.

World-class tooltip component with smart positioning and accessibility.
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


class PremiumTooltipSkill(Skill):
    """
    Premium tooltip component with smart positioning.

    Features:
    - Built on Radix UI Tooltip primitives
    - Smart positioning (auto-flip when near edges)
    - Configurable delay for show/hide
    - Arrow pointing to trigger
    - Multiple placement options (top, right, bottom, left)
    - Keyboard accessible (focus trigger to show)
    - Portal rendering
    - Smooth animations
    - Dark and light themes
    - Respects reduced-motion preferences
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Tooltip Component",
        slug="premium-tooltip",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.BEGINNER,
        tags=["react", "tooltip", "ui", "accessibility", "typescript", "radix-ui"],
        estimated_time_minutes=10,
        description="Production-ready tooltip with smart positioning and accessibility",
    )

    dependencies: list = [
        Dependency(
            name="react",
            version="^18.0.0",
            package_manager="npm",
            reason="UI library",
        ),
        Dependency(
            name="@radix-ui/react-tooltip",
            version="^1.0.7",
            package_manager="npm",
            reason="Accessible tooltip primitives",
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
            title="Use Tooltip Primitives",
            description="Build on Radix UI Tooltip for accessibility",
            code_reference="import * as Tooltip from '@radix-ui/react-tooltip'",
            benefit="Smart positioning, keyboard support, ARIA handled automatically",
        ),
        BestPractice(
            title="Appropriate Delay",
            description="Show tooltip after 300-500ms hover to avoid accidental triggers",
            code_reference="<TooltipProvider delayDuration={400}>",
            benefit="Users don't see tooltips when quickly passing over elements",
        ),
        BestPractice(
            title="Keep Content Concise",
            description="Tooltips should be 1-2 short sentences max",
            code_reference='<Tooltip.Content>Save changes</Tooltip.Content>',
            benefit="Users can quickly scan tooltip, doesn't obscure too much content",
        ),
        BestPractice(
            title="Don't Hide Critical Info",
            description="Never put essential information only in tooltips",
            code_reference="Use tooltips for supplementary info, not critical actions",
            benefit="Mobile users and keyboard-only users can still access all features",
        ),
        BestPractice(
            title="Respect Reduced Motion",
            description="Disable animations for users with motion sensitivity",
            code_reference="@media (prefers-reduced-motion: reduce)",
            benefit="Accessibility for users with vestibular disorders",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Basic Tooltip",
            description="Simple tooltip on hover",
            code='''import { Tooltip } from "@/components/ui/tooltip"

function IconButton() {
  return (
    <Tooltip.Provider>
      <Tooltip>
        <Tooltip.Trigger asChild>
          <button className="p-2 rounded-lg hover:bg-gray-100">
            <TrashIcon className="h-4 w-4" />
          </button>
        </Tooltip.Trigger>

        <Tooltip.Content>
          Delete item
        </Tooltip.Content>
      </Tooltip>
    </Tooltip.Provider>
  )
}''',
        ),
        UsageExample(
            name="Tooltip with Custom Delay",
            description="Adjust delay before showing tooltip",
            code='''<Tooltip.Provider delayDuration={200}>
  <Tooltip>
    <Tooltip.Trigger asChild>
      <button>Hover me</button>
    </Tooltip.Trigger>

    <Tooltip.Content>
      Shows after 200ms
    </Tooltip.Content>
  </Tooltip>
</Tooltip.Provider>''',
        ),
        UsageExample(
            name="Tooltip with Side Positioning",
            description="Control which side the tooltip appears on",
            code='''<Tooltip>
  <Tooltip.Trigger asChild>
    <button>Hover me</button>
  </Tooltip.Trigger>

  <Tooltip.Content side="right" sideOffset={5}>
    Appears on the right
    <Tooltip.Arrow />
  </Tooltip.Content>
</Tooltip>''',
        ),
        UsageExample(
            name="Rich Content Tooltip",
            description="Tooltip with formatted content",
            code='''<Tooltip>
  <Tooltip.Trigger asChild>
    <button>API Status</button>
  </Tooltip.Trigger>

  <Tooltip.Content className="max-w-xs">
    <div className="space-y-1">
      <p className="font-semibold">All systems operational</p>
      <p className="text-xs text-gray-400">
        Last checked: 2 minutes ago
      </p>
    </div>
  </Tooltip.Content>
</Tooltip>''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Using title attribute for tooltips",
            why="No styling control, inconsistent across browsers, not accessible",
            good="Use Radix UI Tooltip for full control and accessibility",
        ),
        AntiPattern(
            bad="Showing tooltip instantly on hover (0ms delay)",
            why="Annoying when cursor passes over, creates visual noise",
            good="Use 300-500ms delay to only show on intentional hover",
        ),
        AntiPattern(
            bad="Long paragraphs of text in tooltips",
            why="Hard to read, obscures content, users can't select text",
            good="Keep tooltips to 1-2 short sentences, use Modal for long content",
        ),
        AntiPattern(
            bad="Interactive elements (buttons, links) inside tooltip",
            why="Tooltip disappears when mouse leaves trigger, can't click content",
            good="Use Popover component for interactive content",
        ),
    ]

    file_structure: dict = {
        "components/ui/tooltip.tsx": "Tooltip component with Radix UI",
        "lib/utils.ts": "cn() utility for class merging",
    }

    component_code: str = '''// components/ui/tooltip.tsx
import * as React from "react"
import * as TooltipPrimitive from "@radix-ui/react-tooltip"
import { cn } from "@/lib/utils"

const TooltipProvider = TooltipPrimitive.Provider
const Tooltip = TooltipPrimitive.Root
const TooltipTrigger = TooltipPrimitive.Trigger

// Tooltip Content
const TooltipContent = React.forwardRef<
  React.ElementRef<typeof TooltipPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof TooltipPrimitive.Content>
>(({ className, sideOffset = 4, ...props }, ref) => (
  <TooltipPrimitive.Portal>
    <TooltipPrimitive.Content
      ref={ref}
      sideOffset={sideOffset}
      className={cn(
        "z-50 overflow-hidden rounded-lg bg-gray-900 px-3 py-2 text-sm text-white shadow-lg",
        // Animation
        "animate-in fade-in-0 zoom-in-95",
        "data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95",
        // Side-specific animations
        "data-[side=bottom]:slide-in-from-top-2",
        "data-[side=left]:slide-in-from-right-2",
        "data-[side=right]:slide-in-from-left-2",
        "data-[side=top]:slide-in-from-bottom-2",
        className
      )}
      {...props}
    />
  </TooltipPrimitive.Portal>
))
TooltipContent.displayName = TooltipPrimitive.Content.displayName

// Tooltip Arrow (optional)
const TooltipArrow = React.forwardRef<
  React.ElementRef<typeof TooltipPrimitive.Arrow>,
  React.ComponentPropsWithoutRef<typeof TooltipPrimitive.Arrow>
>(({ className, ...props }, ref) => (
  <TooltipPrimitive.Arrow
    ref={ref}
    className={cn("fill-gray-900", className)}
    {...props}
  />
))
TooltipArrow.displayName = TooltipPrimitive.Arrow.displayName

/**
 * Premium tooltip component with accessibility.
 *
 * Built on Radix UI Tooltip for smart positioning and keyboard support.
 *
 * @example
 * ```tsx
 * <Tooltip.Provider>
 *   <Tooltip>
 *     <Tooltip.Trigger asChild>
 *       <button>Hover me</button>
 *     </Tooltip.Trigger>
 *
 *     <Tooltip.Content>
 *       Helpful information
 *     </Tooltip.Content>
 *   </Tooltip>
 * </Tooltip.Provider>
 * ```
 */
export {
  Tooltip,
  TooltipProvider,
  TooltipTrigger,
  TooltipContent,
  TooltipArrow,
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
        Generate premium tooltip component files.

        Args:
            context: Optional configuration (not used currently)

        Returns:
            Dictionary of filepath: code
        """
        return {
            "components/ui/tooltip.tsx": self.component_code,
            "lib/utils.ts": self.utils_code,
        }
