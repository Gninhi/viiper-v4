"""
Premium Button Component Skill.

World-class button component following Awwwards standards.
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


class PremiumButtonSkill(Skill):
    """
    Premium button component with variants and accessibility.

    Features:
    - Multiple variants (primary, secondary, ghost, danger, link)
    - Size variants (sm, md, lg)
    - Loading states with spinner
    - Icon support (before/after)
    - Full accessibility (ARIA, keyboard)
    - Smooth animations
    - Type-safe with TypeScript + class-variance-authority
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Button Component",
        slug="premium-button",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["react", "button", "ui", "components", "typescript", "tailwind"],
        estimated_time_minutes=15,
        description="World-class button component with variants, loading states, and full accessibility",
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
            title="Semantic HTML",
            description="Uses semantic <button> element with proper ARIA attributes",
            code_reference='<button aria-busy={loading}>',
            benefit="Better accessibility and SEO",
        ),
        BestPractice(
            title="Type Safety",
            description="Full TypeScript with VariantProps for autocomplete",
            code_reference="VariantProps<typeof buttonVariants>",
            benefit="Catch errors at compile time, great DX",
        ),
        BestPractice(
            title="Loading States",
            description="Visual feedback during async operations",
            code_reference="loading ? <Spinner /> : children",
            benefit="Better UX, users know action is processing",
        ),
        BestPractice(
            title="Focus Management",
            description="Visible focus states for keyboard navigation",
            code_reference="focus-visible:ring-2",
            benefit="Accessibility for keyboard users",
        ),
        BestPractice(
            title="Active Feedback",
            description="Scale down on click for tactile feeling",
            code_reference="active:scale-95",
            benefit="Provides immediate visual feedback",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Primary CTA",
            description="High-emphasis call-to-action button",
            code='<Button variant="primary" size="lg">Get Started Free</Button>',
        ),
        UsageExample(
            name="Form Submit with Loading",
            description="Shows loading state during form submission",
            code='''<form onSubmit={handleSubmit}>
  <Button
    type="submit"
    loading={isSubmitting}
    disabled={!isValid}
  >
    Save Changes
  </Button>
</form>''',
        ),
        UsageExample(
            name="Danger Action with Icon",
            description="Destructive action with confirmation",
            code='''<Button
  variant="danger"
  onClick={handleDelete}
  icon={<TrashIcon />}
>
  Delete Account
</Button>''',
        ),
        UsageExample(
            name="Ghost Navigation",
            description="Minimal button for secondary actions",
            code='<Button variant="ghost" size="sm">Learn More →</Button>',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Using <div> with onClick for clickable elements",
            why="Not keyboard accessible, no semantic meaning, requires extra ARIA",
            good="Always use <button> or <a> for clickable elements",
        ),
        AntiPattern(
            bad="Inline styles for variants (style={{background: isPrimary ? '#000' : '#fff'}})",
            why="Hard to maintain, no type safety, poor DX, inconsistent",
            good="Use class-variance-authority for type-safe, composable variants",
        ),
        AntiPattern(
            bad="No loading state indication during async operations",
            why="Users don't know if their action is processing, may click multiple times",
            good="Show loading spinner and disable button during async operations",
        ),
        AntiPattern(
            bad="Generic colors (#7C3AED purple, #3B82F6 blue)",
            why="Makes your app look like every other startup, no brand identity",
            good="Use unique, premium color palette (e.g., pure black #000, custom accent)",
        ),
    ]

    file_structure: dict = {
        "components/ui/button.tsx": "Button component with variants",
        "lib/utils.ts": "cn() utility for class merging",
    }

    component_code: str = '''// components/ui/button.tsx
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  // Base styles - ALWAYS applied
  "inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        // Primary: High-contrast, bold CTA
        primary:
          "bg-black text-white hover:bg-gray-800 active:scale-95 focus-visible:ring-black",

        // Secondary: Medium emphasis
        secondary:
          "bg-gray-100 text-gray-900 hover:bg-gray-200 active:scale-95 focus-visible:ring-gray-400",

        // Ghost: Minimal, blends with background
        ghost:
          "hover:bg-gray-100 text-gray-700 active:scale-95 focus-visible:ring-gray-400",

        // Danger: Destructive actions (delete, remove)
        danger:
          "bg-red-600 text-white hover:bg-red-700 active:scale-95 focus-visible:ring-red-500",

        // Link: Text-like, no background
        link:
          "text-gray-900 underline-offset-4 hover:underline focus-visible:ring-gray-400",
      },
      size: {
        sm: "h-9 px-3 text-sm",
        md: "h-11 px-5 text-base",
        lg: "h-13 px-7 text-lg",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  /** Button content */
  children: React.ReactNode

  /** Show loading spinner and disable interaction */
  loading?: boolean

  /** Icon to display before content */
  icon?: React.ReactNode

  /** Icon to display after content */
  iconRight?: React.ReactNode
}

/**
 * Premium button component with variants and accessibility.
 *
 * @example
 * ```tsx
 * <Button variant="primary" size="lg">
 *   Get Started
 * </Button>
 *
 * <Button loading={isLoading} onClick={handleSubmit}>
 *   Save Changes
 * </Button>
 * ```
 */
export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant,
      size,
      loading,
      disabled,
      icon,
      iconRight,
      children,
      ...props
    },
    ref
  ) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        disabled={disabled || loading}
        ref={ref}
        aria-busy={loading}
        {...props}
      >
        {loading && (
          <svg
            className="animate-spin h-4 w-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        )}
        {!loading && icon && <span aria-hidden="true">{icon}</span>}
        <span>{children}</span>
        {!loading && iconRight && <span aria-hidden="true">{iconRight}</span>}
      </button>
    )
  }
)

Button.displayName = "Button"
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
        Generate premium button component files.

        Args:
            context: Optional configuration (not used currently)

        Returns:
            Dictionary of filepath: code
        """
        return {
            "components/ui/button.tsx": self.component_code,
            "lib/utils.ts": self.utils_code,
        }
