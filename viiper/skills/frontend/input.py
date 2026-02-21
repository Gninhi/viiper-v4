"""
Premium Input Component Skill with Validation.

World-class input component with validation states and React Hook Form integration.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill,
    SkillMetadata,
    SkillCategory,
    SkillDifficulty,
    BestPractice,
    UsageExample,
    AntiPattern,
)
from viiper.skills.common_dependencies import FRONTEND_FORM_DEPS


class PremiumInputSkill(Skill):
    """
    Premium input component with validation and accessibility.

    Features:
    - Multiple input types (text, email, password, number, tel, url, search)
    - Validation states (default, error, success, warning)
    - Size variants (sm, md, lg)
    - Label, helper text, error message support
    - Icon support (prefix/suffix)
    - React Hook Form integration
    - Full accessibility (ARIA, required indicators)
    - Smooth animations for error states
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Input with Validation",
        slug="premium-input",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["react", "input", "form", "validation", "typescript", "tailwind", "react-hook-form"],
        estimated_time_minutes=20,
        description="Production-ready input component with validation states, React Hook Form integration, and full accessibility",
    )

    dependencies: list = FRONTEND_FORM_DEPS

    best_practices: list = [
        BestPractice(
            title="Semantic HTML with Labels",
            description="Use <label> element properly associated with input via htmlFor",
            code_reference="<label htmlFor={id}>{label}</label>",
            benefit="Screen readers can announce the label when input is focused",
        ),
        BestPractice(
            title="Error Announcements",
            description="Use aria-invalid and aria-describedby for error states",
            code_reference="aria-invalid={!!error} aria-describedby={error ? errorId : undefined}",
            benefit="Assistive technologies announce validation errors",
        ),
        BestPractice(
            title="Required Field Indicators",
            description="Visual and semantic indication of required fields",
            code_reference='required && <span aria-label="required">*</span>',
            benefit="Users know which fields are mandatory before submitting",
        ),
        BestPractice(
            title="Validation on Blur",
            description="Validate after user interaction, not while typing",
            code_reference='mode: "onBlur" // in useForm config',
            benefit="Better UX - doesn't show errors while user is still typing",
        ),
        BestPractice(
            title="Clear Error Messages",
            description="Show specific, actionable error messages",
            code_reference="{error?.message}",
            benefit="Users understand what went wrong and how to fix it",
        ),
        BestPractice(
            title="Type-Safe Validation",
            description="Use Zod schemas for runtime type safety",
            code_reference='z.string().email("Please enter a valid email")',
            benefit="Catch validation errors at runtime with good error messages",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Basic Input with React Hook Form",
            description="Email input with validation",
            code="""import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Input } from "@/components/ui/input"

const schema = z.object({
  email: z.string().email("Please enter a valid email"),
})

function LoginForm() {
  const { register, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
  })

  return (
    <Input
      label="Email"
      type="email"
      {...register("email")}
      error={errors.email}
      required
    />
  )
}""",
        ),
        UsageExample(
            name="Password Input with Visibility Toggle",
            description="Password field with show/hide functionality",
            code="""const [showPassword, setShowPassword] = useState(false)

<Input
  label="Password"
  type={showPassword ? "text" : "password"}
  {...register("password")}
  error={errors.password}
  suffixIcon={
    <button
      type="button"
      onClick={() => setShowPassword(!showPassword)}
    >
      {showPassword ? <EyeOffIcon /> : <EyeIcon />}
    </button>
  }
  required
/>""",
        ),
        UsageExample(
            name="Input with Helper Text",
            description="Input with guidance text below",
            code="""<Input
  label="Username"
  {...register("username")}
  error={errors.username}
  helperText="Use 3-20 characters. Letters, numbers, and underscores only."
/>""",
        ),
        UsageExample(
            name="Input with Prefix Icon",
            description="Search input with icon",
            code="""<Input
  type="search"
  placeholder="Search..."
  prefixIcon={<SearchIcon />}
  size="lg"
/>""",
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="No label, only placeholder text",
            why="Placeholder disappears when typing, inaccessible to screen readers, poor UX",
            good="Always use a visible label with htmlFor attribute",
        ),
        AntiPattern(
            bad="Validate while user is typing (mode: 'onChange')",
            why="Shows errors immediately while user is still entering data, frustrating UX",
            good="Use mode: 'onBlur' or 'onSubmit' to validate after user interaction",
        ),
        AntiPattern(
            bad="Generic error messages ('Invalid input')",
            why="Users don't know what's wrong or how to fix it",
            good="Specific, actionable messages ('Email must include @ symbol')",
        ),
        AntiPattern(
            bad="No visual distinction between states (error, success, disabled)",
            why="Users can't tell if there's a problem or if input is working",
            good="Clear color coding: red for error, green for success, gray for disabled",
        ),
        AntiPattern(
            bad="Not disabling autocomplete for sensitive fields",
            why="Security risk - browsers may save passwords/credit cards",
            good="Use autoComplete='off' or 'new-password' for sensitive fields",
        ),
    ]

    file_structure: dict = {
        "components/ui/input.tsx": "Input component with variants and validation states",
        "lib/utils.ts": "cn() utility for class merging",
    }

    component_code: str = """// components/ui/input.tsx
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const inputVariants = cva(
  // Base styles - ALWAYS applied
  "flex w-full rounded-lg border bg-white px-3 py-2 text-sm transition-all duration-200 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50",
  {
    variants: {
      variant: {
        // Default: Normal state
        default:
          "border-gray-300 focus:border-black focus:ring-black",

        // Error: Validation failed
        error:
          "border-red-500 focus:border-red-600 focus:ring-red-500 bg-red-50",

        // Success: Validation passed
        success:
          "border-green-500 focus:border-green-600 focus:ring-green-500 bg-green-50",

        // Warning: Attention needed
        warning:
          "border-yellow-500 focus:border-yellow-600 focus:ring-yellow-500 bg-yellow-50",
      },
      size: {
        sm: "h-9 text-sm",
        md: "h-11 text-base",
        lg: "h-13 text-lg",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "md",
    },
  }
)

export interface InputProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "size">,
    VariantProps<typeof inputVariants> {
  /** Input label */
  label?: string

  /** Helper text below input */
  helperText?: string

  /** Error object from React Hook Form */
  error?: { message?: string }

  /** Icon before input */
  prefixIcon?: React.ReactNode

  /** Icon after input */
  suffixIcon?: React.ReactNode

  /** Container class name */
  containerClassName?: string

  /** Label class name */
  labelClassName?: string
}

/**
 * Premium input component with validation states.
 *
 * @example
 * ```tsx
 * // With React Hook Form
 * <Input
 *   label="Email"
 *   type="email"
 *   {...register("email")}
 *   error={errors.email}
 *   required
 * />
 *
 * // With prefix icon
 * <Input
 *   label="Search"
 *   prefixIcon={<SearchIcon />}
 * />
 * ```
 */
export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  (
    {
      className,
      variant,
      size,
      label,
      helperText,
      error,
      prefixIcon,
      suffixIcon,
      containerClassName,
      labelClassName,
      id,
      required,
      ...props
    },
    ref
  ) => {
    // Generate unique IDs for accessibility
    const inputId = id || React.useId()
    const errorId = `${inputId}-error`
    const helperId = `${inputId}-helper`

    // Determine variant based on error state
    const effectiveVariant = error ? "error" : variant

    return (
      <div className={cn("flex flex-col gap-1.5", containerClassName)}>
        {/* Label */}
        {label && (
          <label
            htmlFor={inputId}
            className={cn(
              "text-sm font-medium text-gray-900",
              labelClassName
            )}
          >
            {label}
            {required && (
              <span className="ml-1 text-red-500" aria-label="required">
                *
              </span>
            )}
          </label>
        )}

        {/* Input Container */}
        <div className="relative flex items-center">
          {/* Prefix Icon */}
          {prefixIcon && (
            <div className="absolute left-3 flex items-center pointer-events-none text-gray-500">
              {prefixIcon}
            </div>
          )}

          {/* Input Element */}
          <input
            id={inputId}
            ref={ref}
            className={cn(
              inputVariants({ variant: effectiveVariant, size }),
              prefixIcon && "pl-10",
              suffixIcon && "pr-10",
              className
            )}
            aria-invalid={!!error}
            aria-describedby={
              error ? errorId : helperText ? helperId : undefined
            }
            required={required}
            {...props}
          />

          {/* Suffix Icon */}
          {suffixIcon && (
            <div className="absolute right-3 flex items-center text-gray-500">
              {suffixIcon}
            </div>
          )}
        </div>

        {/* Error Message */}
        {error?.message && (
          <p
            id={errorId}
            className="text-sm text-red-600 animate-in slide-in-from-top-1 duration-200"
            role="alert"
          >
            {error.message}
          </p>
        )}

        {/* Helper Text */}
        {helperText && !error && (
          <p id={helperId} className="text-sm text-gray-600">
            {helperText}
          </p>
        )}
      </div>
    )
  }
)

Input.displayName = "Input"
"""

    utils_code: str = """// lib/utils.ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

/**
 * Merge Tailwind CSS classes with proper precedence.
 * Uses clsx for conditional classes and tailwind-merge to handle conflicts.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
"""

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Generate premium input component files.

        Args:
            context: Optional configuration (not used currently)

        Returns:
            Dictionary of filepath: code
        """
        return {
            "components/ui/input.tsx": self.component_code,
            "lib/utils.ts": self.utils_code,
        }
