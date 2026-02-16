"""
Premium Popover Component Skill.

World-class popover component for interactive floating content.
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


class PremiumPopoverSkill(Skill):
    """
    Premium popover component with smart positioning.

    Features:
    - Built on Radix UI Popover primitives
    - Smart collision detection and positioning
    - Interactive content (buttons, forms)
    - Click outside to close
    - ESC key to dismiss
    - Portal rendering
    - Arrow pointing to trigger
    - Controlled and uncontrolled modes
    - Smooth animations
    - Full ARIA attributes
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Popover Component",
        slug="premium-popover",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["react", "popover", "dropdown", "ui", "typescript", "radix-ui"],
        estimated_time_minutes=15,
        description="Production-ready popover with interactive content and smart positioning",
    )

    dependencies: list = [
        Dependency(
            name="react",
            version="^18.0.0",
            package_manager="npm",
            reason="UI library",
        ),
        Dependency(
            name="@radix-ui/react-popover",
            version="^1.0.7",
            package_manager="npm",
            reason="Accessible popover primitives",
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
            title="Use for Interactive Content",
            description="Popover is for interactive content, Tooltip for read-only hints",
            code_reference="Popover for forms/buttons, Tooltip for text hints",
            benefit="Clear distinction prevents UX confusion",
        ),
        BestPractice(
            title="Smart Positioning",
            description="Let Radix handle collision detection automatically",
            code_reference='<Popover.Content side="bottom" align="start">',
            benefit="Popover stays visible even near viewport edges",
        ),
        BestPractice(
            title="Click Outside to Close",
            description="Allow users to dismiss by clicking outside",
            code_reference="Radix handles this automatically",
            benefit="Intuitive dismissal, matches user expectations",
        ),
        BestPractice(
            title="ESC to Close",
            description="Support ESC key for quick dismissal",
            code_reference="Radix handles this automatically",
            benefit="Keyboard users can quickly close popover",
        ),
        BestPractice(
            title="Portal Rendering",
            description="Render in portal to avoid z-index issues",
            code_reference="<Popover.Portal>",
            benefit="Popover always appears above other content",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Basic Popover",
            description="Simple popover with content",
            code='''import { Popover } from "@/components/ui/popover"

function ShareButton() {
  return (
    <Popover>
      <Popover.Trigger asChild>
        <Button variant="secondary">Share</Button>
      </Popover.Trigger>

      <Popover.Content className="w-80">
        <div className="space-y-2">
          <h4 className="font-semibold">Share this page</h4>
          <p className="text-sm text-gray-600">
            Anyone with the link can view this
          </p>
          <Input value="https://example.com/page" readOnly />
        </div>
      </Popover.Content>
    </Popover>
  )
}''',
        ),
        UsageExample(
            name="Popover with Form",
            description="Interactive form inside popover",
            code='''<Popover>
  <Popover.Trigger asChild>
    <Button>Add Comment</Button>
  </Popover.Trigger>

  <Popover.Content className="w-96">
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="text-sm font-medium">Comment</label>
        <textarea
          className="w-full mt-1 rounded-lg border p-2"
          rows={3}
          placeholder="Add your comment..."
        />
      </div>

      <div className="flex justify-end gap-2">
        <Popover.Close asChild>
          <Button variant="ghost">Cancel</Button>
        </Popover.Close>
        <Button type="submit">Post</Button>
      </div>
    </form>
  </Popover.Content>
</Popover>''',
        ),
        UsageExample(
            name="Controlled Popover",
            description="Control popover state externally",
            code='''function ControlledPopover() {
  const [isOpen, setIsOpen] = useState(false)

  const handleAction = () => {
    // Do something
    setIsOpen(false) // Close popover
  }

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <Popover.Trigger asChild>
        <Button>Options</Button>
      </Popover.Trigger>

      <Popover.Content>
        <div className="space-y-2">
          <Button onClick={handleAction} className="w-full">
            Action 1
          </Button>
          <Button onClick={handleAction} className="w-full">
            Action 2
          </Button>
        </div>
      </Popover.Content>
    </Popover>
  )
}''',
        ),
        UsageExample(
            name="Popover Menu",
            description="Dropdown menu using popover",
            code='''<Popover>
  <Popover.Trigger asChild>
    <button className="p-2 rounded-lg hover:bg-gray-100">
      <MoreVerticalIcon className="h-4 w-4" />
    </button>
  </Popover.Trigger>

  <Popover.Content align="end" className="w-48">
    <div className="py-1">
      <button className="w-full px-3 py-2 text-left text-sm hover:bg-gray-100">
        Edit
      </button>
      <button className="w-full px-3 py-2 text-left text-sm hover:bg-gray-100">
        Duplicate
      </button>
      <div className="border-t border-gray-200 my-1" />
      <button className="w-full px-3 py-2 text-left text-sm text-red-600 hover:bg-red-50">
        Delete
      </button>
    </div>
  </Popover.Content>
</Popover>''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Using popover for non-interactive content (just text)",
            why="Overkill, adds unnecessary interaction overhead",
            good="Use Tooltip for read-only hints, Popover for interactive content",
        ),
        AntiPattern(
            bad="No way to close popover from inside (no Cancel button)",
            why="Users get stuck, can only close by clicking outside",
            good="Always provide close/cancel button inside popover",
        ),
        AntiPattern(
            bad="Not using portal rendering",
            why="Popover may be hidden behind other elements due to z-index",
            good="Always render popover in portal",
        ),
        AntiPattern(
            bad="Nesting popovers (popover inside popover)",
            why="Confusing UX, hard to track which is open, dismiss logic breaks",
            good="Avoid nesting, use modal for complex flows",
        ),
    ]

    file_structure: dict = {
        "components/ui/popover.tsx": "Popover component with Radix UI",
        "lib/utils.ts": "cn() utility for class merging",
    }

    component_code: str = '''// components/ui/popover.tsx
import * as React from "react"
import * as PopoverPrimitive from "@radix-ui/react-popover"
import { cn } from "@/lib/utils"

const Popover = PopoverPrimitive.Root
const PopoverTrigger = PopoverPrimitive.Trigger
const PopoverClose = PopoverPrimitive.Close
const PopoverAnchor = PopoverPrimitive.Anchor

// Popover Content
const PopoverContent = React.forwardRef<
  React.ElementRef<typeof PopoverPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof PopoverPrimitive.Content>
>(({ className, align = "center", sideOffset = 4, ...props }, ref) => (
  <PopoverPrimitive.Portal>
    <PopoverPrimitive.Content
      ref={ref}
      align={align}
      sideOffset={sideOffset}
      className={cn(
        "z-50 w-72 rounded-lg border border-gray-200 bg-white p-4 text-gray-900 shadow-lg outline-none",
        // Animation
        "data-[state=open]:animate-in data-[state=open]:fade-in-0 data-[state=open]:zoom-in-95",
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
  </PopoverPrimitive.Portal>
))
PopoverContent.displayName = PopoverPrimitive.Content.displayName

// Popover Arrow (optional)
const PopoverArrow = React.forwardRef<
  React.ElementRef<typeof PopoverPrimitive.Arrow>,
  React.ComponentPropsWithoutRef<typeof PopoverPrimitive.Arrow>
>(({ className, ...props }, ref) => (
  <PopoverPrimitive.Arrow
    ref={ref}
    className={cn("fill-white", className)}
    {...props}
  />
))
PopoverArrow.displayName = PopoverPrimitive.Arrow.displayName

/**
 * Premium popover component with accessibility.
 *
 * Built on Radix UI Popover for smart positioning and interaction.
 *
 * Use for interactive content (forms, buttons).
 * For read-only hints, use Tooltip instead.
 *
 * @example
 * ```tsx
 * <Popover>
 *   <Popover.Trigger asChild>
 *     <Button>Open</Button>
 *   </Popover.Trigger>
 *
 *   <Popover.Content>
 *     <p>Interactive content here</p>
 *   </Popover.Content>
 * </Popover>
 * ```
 */
export {
  Popover,
  PopoverTrigger,
  PopoverContent,
  PopoverClose,
  PopoverAnchor,
  PopoverArrow,
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
        Generate premium popover component files.

        Args:
            context: Optional configuration (not used currently)

        Returns:
            Dictionary of filepath: code
        """
        return {
            "components/ui/popover.tsx": self.component_code,
            "lib/utils.ts": self.utils_code,
        }
