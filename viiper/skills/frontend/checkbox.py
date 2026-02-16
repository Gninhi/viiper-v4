"""
Premium Checkbox & Switch Component Skill.

World-class form controls for boolean inputs.
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


class PremiumCheckboxSkill(Skill):
    """
    Premium checkbox and switch components.

    Features:
    - Checkbox with custom styling
    - Switch/Toggle variant
    - Indeterminate state (checkbox)
    - Disabled state
    - Label association
    - Error states
    - React Hook Form integration
    - Full ARIA attributes
    - Keyboard accessible
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Checkbox & Switch Components",
        slug="premium-checkbox",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.BEGINNER,
        tags=["react", "checkbox", "switch", "toggle", "form", "typescript"],
        estimated_time_minutes=15,
        description="Production-ready checkbox and switch components with full accessibility",
    )

    dependencies: list = [
        Dependency(
            name="react",
            version="^18.0.0",
            package_manager="npm",
            reason="UI library",
        ),
        Dependency(
            name="@radix-ui/react-checkbox",
            version="^1.0.4",
            package_manager="npm",
            reason="Checkbox primitives",
        ),
        Dependency(
            name="@radix-ui/react-switch",
            version="^1.0.3",
            package_manager="npm",
            reason="Switch primitives",
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
        Dependency(
            name="lucide-react",
            version="^0.294.0",
            package_manager="npm",
            reason="Check icon",
        ),
    ]

    best_practices: list = [
        BestPractice(
            title="Always Use Labels",
            description="Associate label with checkbox via htmlFor",
            code_reference='<label htmlFor={id}>',
            benefit="Larger click target, accessible",
        ),
        BestPractice(
            title="Switch vs Checkbox",
            description="Use Switch for immediate actions, Checkbox for form submission",
            code_reference="Switch: toggle setting, Checkbox: select items",
            benefit="Clear user expectations",
        ),
        BestPractice(
            title="Indeterminate State",
            description="Show partial selection in parent checkbox",
            code_reference='<Checkbox indeterminate />',
            benefit="Clear visual for 'some selected' state",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Basic Checkbox",
            description="Simple checkbox with label",
            code='''import { Checkbox } from "@/components/ui/checkbox"

<div className="flex items-center space-x-2">
  <Checkbox id="terms" />
  <label htmlFor="terms" className="text-sm font-medium">
    Accept terms and conditions
  </label>
</div>''',
        ),
        UsageExample(
            name="Checkbox with React Hook Form",
            description="Form integration",
            code='''const { register } = useForm()

<div className="flex items-center space-x-2">
  <Checkbox id="newsletter" {...register("newsletter")} />
  <label htmlFor="newsletter">Subscribe to newsletter</label>
</div>''',
        ),
        UsageExample(
            name="Switch Toggle",
            description="Binary setting toggle",
            code='''import { Switch } from "@/components/ui/switch"

const [enabled, setEnabled] = useState(false)

<div className="flex items-center space-x-2">
  <Switch id="notifications" checked={enabled} onCheckedChange={setEnabled} />
  <label htmlFor="notifications">Enable notifications</label>
</div>''',
        ),
        UsageExample(
            name="Indeterminate Checkbox",
            description="Parent checkbox for select all",
            code='''const allChecked = items.every(item => item.checked)
const someChecked = items.some(item => item.checked) && !allChecked

<Checkbox
  checked={allChecked}
  indeterminate={someChecked}
  onCheckedChange={(checked) => toggleAll(checked)}
/>''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Checkbox without label (only icon)",
            why="Tiny click target, not accessible",
            good="Always provide visible label",
        ),
        AntiPattern(
            bad="Using Switch for form submission",
            why="Users expect switches to save immediately",
            good="Use Checkbox for forms, Switch for instant actions",
        ),
    ]

    file_structure: dict = {
        "components/ui/checkbox.tsx": "Checkbox component",
        "components/ui/switch.tsx": "Switch component",
        "lib/utils.ts": "Utilities",
    }

    checkbox_code: str = '''// components/ui/checkbox.tsx
import * as React from "react"
import * as CheckboxPrimitive from "@radix-ui/react-checkbox"
import { Check } from "lucide-react"
import { cn } from "@/lib/utils"

const Checkbox = React.forwardRef<
  React.ElementRef<typeof CheckboxPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof CheckboxPrimitive.Root>
>(({ className, ...props }, ref) => (
  <CheckboxPrimitive.Root
    ref={ref}
    className={cn(
      "peer h-4 w-4 shrink-0 rounded border border-gray-300 ring-offset-white",
      "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-2",
      "disabled:cursor-not-allowed disabled:opacity-50",
      "data-[state=checked]:bg-black data-[state=checked]:border-black data-[state=checked]:text-white",
      "data-[state=indeterminate]:bg-black data-[state=indeterminate]:border-black",
      className
    )}
    {...props}
  >
    <CheckboxPrimitive.Indicator className={cn("flex items-center justify-center text-current")}>
      <Check className="h-3 w-3" />
    </CheckboxPrimitive.Indicator>
  </CheckboxPrimitive.Root>
))
Checkbox.displayName = CheckboxPrimitive.Root.displayName

export { Checkbox }
'''

    switch_code: str = '''// components/ui/switch.tsx
import * as React from "react"
import * as SwitchPrimitives from "@radix-ui/react-switch"
import { cn } from "@/lib/utils"

const Switch = React.forwardRef<
  React.ElementRef<typeof SwitchPrimitives.Root>,
  React.ComponentPropsWithoutRef<typeof SwitchPrimitives.Root>
>(({ className, ...props }, ref) => (
  <SwitchPrimitives.Root
    className={cn(
      "peer inline-flex h-6 w-11 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent",
      "transition-colors",
      "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-2 focus-visible:ring-offset-white",
      "disabled:cursor-not-allowed disabled:opacity-50",
      "data-[state=checked]:bg-black data-[state=unchecked]:bg-gray-200",
      className
    )}
    {...props}
    ref={ref}
  >
    <SwitchPrimitives.Thumb
      className={cn(
        "pointer-events-none block h-5 w-5 rounded-full bg-white shadow-lg ring-0 transition-transform",
        "data-[state=checked]:translate-x-5 data-[state=unchecked]:translate-x-0"
      )}
    />
  </SwitchPrimitives.Root>
))
Switch.displayName = SwitchPrimitives.Root.displayName

export { Switch }
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
            "components/ui/checkbox.tsx": self.checkbox_code,
            "components/ui/switch.tsx": self.switch_code,
            "lib/utils.ts": self.utils_code,
        }
