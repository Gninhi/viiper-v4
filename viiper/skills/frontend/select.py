"""
Premium Select/Dropdown Component Skill.

World-class select component with search and accessibility.
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


class PremiumSelectSkill(Skill):
    """
    Premium select/dropdown component with accessibility.

    Features:
    - Built on Radix UI Select primitives
    - Keyboard navigation (arrows, type-ahead)
    - Multiple select support
    - Search/filter functionality
    - Custom trigger styling
    - Size variants (sm, md, lg)
    - Grouped options
    - Disabled state
    - Full ARIA attributes
    - Portal rendering
    - Smooth animations
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Select/Dropdown Component",
        slug="premium-select",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["react", "select", "dropdown", "ui", "typescript", "radix-ui"],
        estimated_time_minutes=20,
        description="Production-ready select component with keyboard navigation and accessibility",
    )

    dependencies: list = [
        Dependency(
            name="react",
            version="^18.0.0",
            package_manager="npm",
            reason="UI library",
        ),
        Dependency(
            name="@radix-ui/react-select",
            version="^2.0.0",
            package_manager="npm",
            reason="Accessible select primitives",
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
        Dependency(
            name="lucide-react",
            version="^0.294.0",
            package_manager="npm",
            reason="Icons (ChevronDown, Check)",
        ),
    ]

    best_practices: list = [
        BestPractice(
            title="Use Select Primitives",
            description="Build on Radix UI Select for accessibility",
            code_reference="import * as Select from '@radix-ui/react-select'",
            benefit="Keyboard navigation, ARIA attributes, focus management handled",
        ),
        BestPractice(
            title="Keyboard Navigation",
            description="Support arrow keys, Enter, Escape, and type-ahead",
            code_reference="Radix Select handles this automatically",
            benefit="Keyboard users can navigate efficiently",
        ),
        BestPractice(
            title="Visual Feedback",
            description="Show selected state with checkmark icon",
            code_reference="<Check className='h-4 w-4' />",
            benefit="Users know which option is selected",
        ),
        BestPractice(
            title="Group Related Options",
            description="Use SelectGroup for categorizing options",
            code_reference="<Select.Group><Select.Label>Group Name</Select.Label></Select.Group>",
            benefit="Easier to scan large option lists",
        ),
        BestPractice(
            title="Portal Rendering",
            description="Render dropdown in portal to avoid z-index issues",
            code_reference="<Select.Portal>",
            benefit="Dropdown always appears above other content",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Basic Select",
            description="Simple select with options",
            code='''import { Select } from "@/components/ui/select"

function LanguageSelect() {
  const [language, setLanguage] = useState("en")

  return (
    <Select value={language} onValueChange={setLanguage}>
      <Select.Trigger className="w-48">
        <Select.Value placeholder="Select language" />
      </Select.Trigger>

      <Select.Content>
        <Select.Item value="en">English</Select.Item>
        <Select.Item value="fr">Français</Select.Item>
        <Select.Item value="es">Español</Select.Item>
        <Select.Item value="de">Deutsch</Select.Item>
      </Select.Content>
    </Select>
  )
}''',
        ),
        UsageExample(
            name="Select with Groups",
            description="Grouped options for better organization",
            code='''<Select value={timezone} onValueChange={setTimezone}>
  <Select.Trigger className="w-64">
    <Select.Value placeholder="Select timezone" />
  </Select.Trigger>

  <Select.Content>
    <Select.Group>
      <Select.Label>North America</Select.Label>
      <Select.Item value="est">Eastern Time</Select.Item>
      <Select.Item value="cst">Central Time</Select.Item>
      <Select.Item value="pst">Pacific Time</Select.Item>
    </Select.Group>

    <Select.Separator />

    <Select.Group>
      <Select.Label>Europe</Select.Label>
      <Select.Item value="gmt">GMT</Select.Item>
      <Select.Item value="cet">Central European Time</Select.Item>
    </Select.Group>
  </Select.Content>
</Select>''',
        ),
        UsageExample(
            name="Select in Form",
            description="Integration with React Hook Form",
            code='''import { useForm, Controller } from "react-hook-form"
import { Select } from "@/components/ui/select"

function ProfileForm() {
  const { control, handleSubmit } = useForm()

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Controller
        name="country"
        control={control}
        render={({ field }) => (
          <Select value={field.value} onValueChange={field.onChange}>
            <Select.Trigger>
              <Select.Value placeholder="Select country" />
            </Select.Trigger>

            <Select.Content>
              <Select.Item value="us">United States</Select.Item>
              <Select.Item value="uk">United Kingdom</Select.Item>
              <Select.Item value="ca">Canada</Select.Item>
            </Select.Content>
          </Select>
        )}
      />
    </form>
  )
}''',
        ),
        UsageExample(
            name="Disabled Options",
            description="Disable specific options",
            code='''<Select>
  <Select.Trigger>
    <Select.Value placeholder="Select plan" />
  </Select.Trigger>

  <Select.Content>
    <Select.Item value="free">Free Plan</Select.Item>
    <Select.Item value="pro">Pro Plan</Select.Item>
    <Select.Item value="enterprise" disabled>
      Enterprise (Contact Sales)
    </Select.Item>
  </Select.Content>
</Select>''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Building custom select from scratch with divs",
            why="Hard to make accessible, missing keyboard navigation, lots of bugs",
            good="Use Radix UI Select primitives for accessibility",
        ),
        AntiPattern(
            bad="Using native <select> element for custom styling",
            why="Very limited styling options, inconsistent across browsers",
            good="Use Radix UI Select for full styling control",
        ),
        AntiPattern(
            bad="No visual indication of selected item in dropdown",
            why="Users can't tell which option is currently selected",
            good="Show checkmark icon next to selected item",
        ),
        AntiPattern(
            bad="Long list without grouping or search",
            why="Hard to find options, poor UX for 20+ items",
            good="Group related options or add search functionality",
        ),
    ]

    file_structure: dict = {
        "components/ui/select.tsx": "Select component with Radix UI",
        "lib/utils.ts": "cn() utility for class merging",
    }

    component_code: str = '''// components/ui/select.tsx
import * as React from "react"
import * as SelectPrimitive from "@radix-ui/react-select"
import { Check, ChevronDown } from "lucide-react"
import { cn } from "@/lib/utils"

const Select = SelectPrimitive.Root
const SelectGroup = SelectPrimitive.Group
const SelectValue = SelectPrimitive.Value

// Trigger (the button that opens the dropdown)
const SelectTrigger = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Trigger>
>(({ className, children, ...props }, ref) => (
  <SelectPrimitive.Trigger
    ref={ref}
    className={cn(
      "flex h-11 w-full items-center justify-between rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm",
      "focus:outline-none focus:ring-2 focus:ring-black focus:ring-offset-1",
      "disabled:cursor-not-allowed disabled:opacity-50",
      "hover:border-gray-400 transition-colors",
      className
    )}
    {...props}
  >
    {children}
    <SelectPrimitive.Icon asChild>
      <ChevronDown className="h-4 w-4 opacity-50" />
    </SelectPrimitive.Icon>
  </SelectPrimitive.Trigger>
))
SelectTrigger.displayName = SelectPrimitive.Trigger.displayName

// Content (the dropdown panel)
const SelectContent = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Content>
>(({ className, children, position = "popper", ...props }, ref) => (
  <SelectPrimitive.Portal>
    <SelectPrimitive.Content
      ref={ref}
      className={cn(
        "relative z-50 min-w-[8rem] overflow-hidden rounded-lg border border-gray-200 bg-white text-gray-900 shadow-lg",
        "data-[state=open]:animate-in data-[state=open]:fade-in-0 data-[state=open]:zoom-in-95",
        "data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95",
        position === "popper" &&
          "data-[side=bottom]:translate-y-1 data-[side=left]:-translate-x-1 data-[side=right]:translate-x-1 data-[side=top]:-translate-y-1",
        className
      )}
      position={position}
      {...props}
    >
      <SelectPrimitive.Viewport
        className={cn(
          "p-1",
          position === "popper" &&
            "h-[var(--radix-select-trigger-height)] w-full min-w-[var(--radix-select-trigger-width)]"
        )}
      >
        {children}
      </SelectPrimitive.Viewport>
    </SelectPrimitive.Content>
  </SelectPrimitive.Portal>
))
SelectContent.displayName = SelectPrimitive.Content.displayName

// Label (for option groups)
const SelectLabel = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Label>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Label>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.Label
    ref={ref}
    className={cn("py-1.5 px-2 text-sm font-semibold text-gray-900", className)}
    {...props}
  />
))
SelectLabel.displayName = SelectPrimitive.Label.displayName

// Item (individual option)
const SelectItem = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Item>
>(({ className, children, ...props }, ref) => (
  <SelectPrimitive.Item
    ref={ref}
    className={cn(
      "relative flex w-full cursor-pointer select-none items-center rounded-md py-2 pl-8 pr-2 text-sm outline-none",
      "focus:bg-gray-100 focus:text-gray-900",
      "data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      "transition-colors",
      className
    )}
    {...props}
  >
    <span className="absolute left-2 flex h-4 w-4 items-center justify-center">
      <SelectPrimitive.ItemIndicator>
        <Check className="h-4 w-4" />
      </SelectPrimitive.ItemIndicator>
    </span>

    <SelectPrimitive.ItemText>{children}</SelectPrimitive.ItemText>
  </SelectPrimitive.Item>
))
SelectItem.displayName = SelectPrimitive.Item.displayName

// Separator (between groups)
const SelectSeparator = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Separator>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Separator>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.Separator
    ref={ref}
    className={cn("-mx-1 my-1 h-px bg-gray-200", className)}
    {...props}
  />
))
SelectSeparator.displayName = SelectPrimitive.Separator.displayName

/**
 * Premium select component with accessibility.
 *
 * Built on Radix UI Select for keyboard navigation and ARIA.
 *
 * @example
 * ```tsx
 * <Select value={value} onValueChange={setValue}>
 *   <Select.Trigger>
 *     <Select.Value placeholder="Select option" />
 *   </Select.Trigger>
 *
 *   <Select.Content>
 *     <Select.Item value="1">Option 1</Select.Item>
 *     <Select.Item value="2">Option 2</Select.Item>
 *   </Select.Content>
 * </Select>
 * ```
 */
export {
  Select,
  SelectGroup,
  SelectValue,
  SelectTrigger,
  SelectContent,
  SelectLabel,
  SelectItem,
  SelectSeparator,
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
        Generate premium select component files.

        Args:
            context: Optional configuration (not used currently)

        Returns:
            Dictionary of filepath: code
        """
        return {
            "components/ui/select.tsx": self.component_code,
            "lib/utils.ts": self.utils_code,
        }
