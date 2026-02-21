"""
Premium Accordion Component Skill.

World-class accordion/collapsible component with smooth animations.
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
from viiper.skills.common_dependencies import FRONTEND_BASE_DEPS


class PremiumAccordionSkill(Skill):
    """
    Premium accordion component with accessibility.

    Features:
    - Built on Radix UI Accordion primitives
    - Single or multiple open items
    - Smooth expand/collapse animations
    - Keyboard navigation (arrows, Home, End)
    - Icon rotation on expand
    - Controlled and uncontrolled modes
    - Full ARIA attributes
    - Collapsible variant (all items can close)
    - Disabled items support
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Accordion Component",
        slug="premium-accordion",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.BEGINNER,
        tags=["react", "accordion", "collapsible", "ui", "typescript", "radix-ui"],
        estimated_time_minutes=15,
        description="Production-ready accordion with smooth animations and accessibility",
    )

    dependencies: list = FRONTEND_BASE_DEPS + [
        Dependency(
            name="@radix-ui/react-accordion",
            version="^1.1.2",
            package_manager="npm",
            reason="Accessible accordion primitives",
        ),
    ]

    best_practices: list = [
        BestPractice(
            title="Use Accordion Primitives",
            description="Build on Radix UI for accessibility",
            code_reference="import * as Accordion from '@radix-ui/react-accordion'",
            benefit="Keyboard navigation, ARIA, focus management handled automatically",
        ),
        BestPractice(
            title="Smooth Animations",
            description="Animate height changes with CSS transitions",
            code_reference="data-[state=open]:animate-accordion-down",
            benefit="Professional feel, users can track content appearance",
        ),
        BestPractice(
            title="Visual Expand Indicator",
            description="Rotate chevron icon to show open/closed state",
            code_reference="data-[state=open]:rotate-180",
            benefit="Clear visual feedback of accordion state",
        ),
        BestPractice(
            title="Single vs Multiple",
            description="Choose type='single' or 'multiple' based on use case",
            code_reference="<Accordion type='single' collapsible>",
            benefit="Single for FAQs (one answer at a time), Multiple for filters",
        ),
        BestPractice(
            title="Keyboard Navigation",
            description="Support arrow keys, Home, End for navigation",
            code_reference="Radix handles this automatically",
            benefit="Keyboard users can efficiently navigate items",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Basic FAQ Accordion",
            description="Single-item accordion for FAQs",
            code='''import { Accordion } from "@/components/ui/accordion"

function FAQ() {
  return (
    <Accordion type="single" collapsible>
      <Accordion.Item value="item-1">
        <Accordion.Trigger>
          What is your return policy?
        </Accordion.Trigger>
        <Accordion.Content>
          We offer a 30-day money-back guarantee on all products.
          No questions asked.
        </Accordion.Content>
      </Accordion.Item>

      <Accordion.Item value="item-2">
        <Accordion.Trigger>
          How long does shipping take?
        </Accordion.Trigger>
        <Accordion.Content>
          Standard shipping takes 3-5 business days.
          Express shipping is available for 1-2 day delivery.
        </Accordion.Content>
      </Accordion.Item>

      <Accordion.Item value="item-3">
        <Accordion.Trigger>
          Do you ship internationally?
        </Accordion.Trigger>
        <Accordion.Content>
          Yes! We ship to over 100 countries worldwide.
        </Accordion.Content>
      </Accordion.Item>
    </Accordion>
  )
}''',
        ),
        UsageExample(
            name="Multiple Open Items",
            description="Allow multiple sections to be open at once",
            code='''<Accordion type="multiple">
  <Accordion.Item value="personal">
    <Accordion.Trigger>Personal Information</Accordion.Trigger>
    <Accordion.Content>
      <Input label="Name" />
      <Input label="Email" />
    </Accordion.Content>
  </Accordion.Item>

  <Accordion.Item value="address">
    <Accordion.Trigger>Shipping Address</Accordion.Trigger>
    <Accordion.Content>
      <Input label="Street" />
      <Input label="City" />
    </Accordion.Content>
  </Accordion.Item>
</Accordion>''',
        ),
        UsageExample(
            name="Controlled Accordion",
            description="Control accordion state externally",
            code='''function ControlledAccordion() {
  const [value, setValue] = useState("item-1")

  return (
    <div>
      <Accordion type="single" value={value} onValueChange={setValue}>
        <Accordion.Item value="item-1">
          <Accordion.Trigger>Section 1</Accordion.Trigger>
          <Accordion.Content>Content 1</Accordion.Content>
        </Accordion.Item>

        <Accordion.Item value="item-2">
          <Accordion.Trigger>Section 2</Accordion.Trigger>
          <Accordion.Content>Content 2</Accordion.Content>
        </Accordion.Item>
      </Accordion>

      <p className="mt-4 text-sm">Open: {value}</p>
    </div>
  )
}''',
        ),
        UsageExample(
            name="Disabled Item",
            description="Disable specific accordion items",
            code='''<Accordion type="single" collapsible>
  <Accordion.Item value="item-1">
    <Accordion.Trigger>Available Section</Accordion.Trigger>
    <Accordion.Content>This content is available</Accordion.Content>
  </Accordion.Item>

  <Accordion.Item value="item-2" disabled>
    <Accordion.Trigger>Premium Feature (Upgrade Required)</Accordion.Trigger>
    <Accordion.Content>Premium content</Accordion.Content>
  </Accordion.Item>
</Accordion>''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Building accordion with manual state and onClick handlers",
            why="Missing keyboard navigation, ARIA, complex state management",
            good="Use Radix UI Accordion for built-in accessibility",
        ),
        AntiPattern(
            bad="Instant expand/collapse with no animation",
            why="Jarring, users lose track of content, feels unpolished",
            good="Smooth height animation with CSS transitions",
        ),
        AntiPattern(
            bad="No visual indicator of open/closed state",
            why="Users can't tell if item is expanded, confusing UX",
            good="Rotate chevron icon on expand",
        ),
        AntiPattern(
            bad="Nesting accordions deeply (accordion inside accordion)",
            why="Confusing navigation, hard to track depth, poor UX",
            good="Keep accordion structure flat, use tabs for complex hierarchies",
        ),
    ]

    file_structure: dict = {
        "components/ui/accordion.tsx": "Accordion component with Radix UI",
        "lib/utils.ts": "cn() utility for class merging",
    }

    component_code: str = '''// components/ui/accordion.tsx
import * as React from "react"
import * as AccordionPrimitive from "@radix-ui/react-accordion"
import { ChevronDown } from "lucide-react"
import { cn } from "@/lib/utils"

const Accordion = AccordionPrimitive.Root

// Accordion Item
const AccordionItem = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Item>
>(({ className, ...props }, ref) => (
  <AccordionPrimitive.Item
    ref={ref}
    className={cn("border-b border-gray-200", className)}
    {...props}
  />
))
AccordionItem.displayName = "AccordionItem"

// Accordion Trigger (the clickable header)
const AccordionTrigger = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Trigger>
>(({ className, children, ...props }, ref) => (
  <AccordionPrimitive.Header className="flex">
    <AccordionPrimitive.Trigger
      ref={ref}
      className={cn(
        "flex flex-1 items-center justify-between py-4 text-left font-medium transition-all",
        "hover:text-gray-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-2",
        "disabled:cursor-not-allowed disabled:opacity-50",
        "[&[data-state=open]>svg]:rotate-180",
        className
      )}
      {...props}
    >
      {children}
      <ChevronDown className="h-4 w-4 shrink-0 text-gray-600 transition-transform duration-200" />
    </AccordionPrimitive.Trigger>
  </AccordionPrimitive.Header>
))
AccordionTrigger.displayName = AccordionPrimitive.Trigger.displayName

// Accordion Content (the expandable content)
const AccordionContent = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <AccordionPrimitive.Content
    ref={ref}
    className={cn(
      "overflow-hidden text-sm text-gray-600 transition-all",
      "data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down",
      className
    )}
    {...props}
  >
    <div className="pb-4 pt-0">{children}</div>
  </AccordionPrimitive.Content>
))
AccordionContent.displayName = AccordionPrimitive.Content.displayName

/**
 * Premium accordion component with accessibility.
 *
 * Built on Radix UI Accordion for keyboard navigation and ARIA.
 *
 * @example
 * ```tsx
 * <Accordion type="single" collapsible>
 *   <Accordion.Item value="item-1">
 *     <Accordion.Trigger>Question?</Accordion.Trigger>
 *     <Accordion.Content>Answer</Accordion.Content>
 *   </Accordion.Item>
 * </Accordion>
 * ```
 */
export { Accordion, AccordionItem, AccordionTrigger, AccordionContent }
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

    tailwind_config: str = '''// tailwind.config.js
// Add these animations to your Tailwind config

module.exports = {
  theme: {
    extend: {
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
}
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Generate premium accordion component files.

        Args:
            context: Optional configuration (not used currently)

        Returns:
            Dictionary of filepath: code
        """
        return {
            "components/ui/accordion.tsx": self.component_code,
            "lib/utils.ts": self.utils_code,
            "tailwind.config.js": self.tailwind_config,
        }
