"""
Premium Form with Zod Validation Skill.

Complete form implementation pattern with type-safe validation.
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


class PremiumFormSkill(Skill):
    """
    Premium form pattern with React Hook Form and Zod validation.

    Features:
    - Type-safe validation with Zod schemas
    - Form state management with React Hook Form
    - Automatic error handling and display
    - Field-level and form-level validation
    - Async validation support
    - Loading states during submission
    - Success/error feedback
    - Form reset after submission
    - Accessible error announcements
    - Composable with Input, Button, Select components
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Form with Zod Validation",
        slug="premium-form-zod",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.ADVANCED,
        tags=["react", "form", "validation", "zod", "react-hook-form", "typescript"],
        estimated_time_minutes=30,
        description="Complete form implementation pattern with type-safe Zod validation and React Hook Form",
    )

    dependencies: list = FRONTEND_BASE_DEPS

    best_practices: list = [
        BestPractice(
            title="Type-Safe Schemas",
            description="Define Zod schemas and infer TypeScript types from them",
            code_reference='type FormData = z.infer<typeof formSchema>',
            benefit="Single source of truth - validation rules and types stay in sync",
        ),
        BestPractice(
            title="Validate on Blur",
            description="Set validation mode to 'onBlur' for better UX",
            code_reference="useForm({ mode: 'onBlur' })",
            benefit="Users aren't interrupted while typing, only see errors after leaving field",
        ),
        BestPractice(
            title="Specific Error Messages",
            description="Provide clear, actionable error messages in Zod schema",
            code_reference='z.string().min(8, "Password must be at least 8 characters")',
            benefit="Users understand exactly what's wrong and how to fix it",
        ),
        BestPractice(
            title="Loading States",
            description="Show loading indicator during async submission",
            code_reference='<Button loading={isSubmitting}>',
            benefit="Users know their action is processing, prevents double submissions",
        ),
        BestPractice(
            title="Reset After Success",
            description="Reset form state after successful submission",
            code_reference="reset() after successful submit",
            benefit="Clean slate for next submission, clear success indication",
        ),
        BestPractice(
            title="Form-Level Errors",
            description="Handle and display API/server errors separately from field errors",
            code_reference="setError('root', { message: apiError })",
            benefit="Distinguish between client-side validation and server errors",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Login Form",
            description="Simple login form with email and password validation",
            code='''import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const loginSchema = z.object({
  email: z.string().email("Please enter a valid email"),
  password: z.string().min(8, "Password must be at least 8 characters"),
})

type LoginFormData = z.infer<typeof loginSchema>

export function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    mode: "onBlur",
  })

  const onSubmit = async (data: LoginFormData) => {
    try {
      await api.login(data)
      // Handle success
    } catch (error) {
      // Handle error
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <Input
        label="Email"
        type="email"
        {...register("email")}
        error={errors.email}
        required
      />

      <Input
        label="Password"
        type="password"
        {...register("password")}
        error={errors.password}
        required
      />

      <Button type="submit" loading={isSubmitting} className="w-full">
        Sign In
      </Button>
    </form>
  )
}''',
        ),
        UsageExample(
            name="Registration Form with Confirmation",
            description="Registration form with password confirmation validation",
            code='''const registerSchema = z.object({
  email: z.string().email("Please enter a valid email"),
  password: z.string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Password must contain at least one uppercase letter")
    .regex(/[0-9]/, "Password must contain at least one number"),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"], // Error shows on confirmPassword field
})

type RegisterFormData = z.infer<typeof registerSchema>

export function RegisterForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting }, reset } =
    useForm<RegisterFormData>({
      resolver: zodResolver(registerSchema),
      mode: "onBlur",
    })

  const onSubmit = async (data: RegisterFormData) => {
    try {
      await api.register(data)
      reset() // Clear form after success
      toast.success("Account created successfully!")
    } catch (error) {
      toast.error("Registration failed. Please try again.")
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <Input
        label="Email"
        type="email"
        {...register("email")}
        error={errors.email}
        required
      />

      <Input
        label="Password"
        type="password"
        {...register("password")}
        error={errors.password}
        required
      />

      <Input
        label="Confirm Password"
        type="password"
        {...register("confirmPassword")}
        error={errors.confirmPassword}
        required
      />

      <Button type="submit" loading={isSubmitting} className="w-full">
        Create Account
      </Button>
    </form>
  )
}''',
        ),
        UsageExample(
            name="Profile Form with Nested Fields",
            description="Complex form with nested objects and arrays",
            code='''const profileSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  bio: z.string().max(500, "Bio must be 500 characters or less").optional(),
  social: z.object({
    twitter: z.string().url("Must be a valid URL").optional(),
    github: z.string().url("Must be a valid URL").optional(),
  }),
  skills: z.array(z.string()).min(1, "Select at least one skill"),
})

type ProfileFormData = z.infer<typeof profileSchema>

export function ProfileForm({ defaultValues }: { defaultValues?: ProfileFormData }) {
  const { register, handleSubmit, formState: { errors, isSubmitting, isDirty } } =
    useForm<ProfileFormData>({
      resolver: zodResolver(profileSchema),
      defaultValues,
      mode: "onBlur",
    })

  const onSubmit = async (data: ProfileFormData) => {
    try {
      await api.updateProfile(data)
      toast.success("Profile updated!")
    } catch (error) {
      toast.error("Update failed. Please try again.")
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <Input
        label="Name"
        {...register("name")}
        error={errors.name}
        required
      />

      <div className="space-y-4">
        <label className="text-sm font-medium">Bio</label>
        <textarea
          {...register("bio")}
          className="w-full rounded-lg border border-gray-300 p-3"
          rows={4}
        />
        {errors.bio && (
          <p className="text-sm text-red-600">{errors.bio.message}</p>
        )}
      </div>

      <div className="space-y-4">
        <h3 className="text-sm font-medium">Social Links</h3>

        <Input
          label="Twitter"
          type="url"
          {...register("social.twitter")}
          error={errors.social?.twitter}
        />

        <Input
          label="GitHub"
          type="url"
          {...register("social.github")}
          error={errors.social?.github}
        />
      </div>

      <Button
        type="submit"
        loading={isSubmitting}
        disabled={!isDirty}
      >
        Save Changes
      </Button>
    </form>
  )
}''',
        ),
        UsageExample(
            name="Form with Server-Side Validation",
            description="Handling API errors and displaying them",
            code='''export function ContactForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setError,
  } = useForm<ContactFormData>({
    resolver: zodResolver(contactSchema),
    mode: "onBlur",
  })

  const onSubmit = async (data: ContactFormData) => {
    try {
      const response = await api.sendMessage(data)
      toast.success("Message sent successfully!")
    } catch (error) {
      // Handle field-specific errors from API
      if (error.fieldErrors) {
        Object.entries(error.fieldErrors).forEach(([field, message]) => {
          setError(field as keyof ContactFormData, {
            type: "server",
            message: message as string,
          })
        })
      } else {
        // Handle general errors
        setError("root", {
          type: "server",
          message: error.message || "Something went wrong. Please try again.",
        })
      }
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {errors.root && (
        <div className="rounded-lg bg-red-50 border border-red-200 p-4">
          <p className="text-sm text-red-600">{errors.root.message}</p>
        </div>
      )}

      <Input
        label="Name"
        {...register("name")}
        error={errors.name}
        required
      />

      <Input
        label="Email"
        type="email"
        {...register("email")}
        error={errors.email}
        required
      />

      <div className="space-y-2">
        <label className="text-sm font-medium">Message</label>
        <textarea
          {...register("message")}
          className="w-full rounded-lg border border-gray-300 p-3"
          rows={6}
        />
        {errors.message && (
          <p className="text-sm text-red-600">{errors.message.message}</p>
        )}
      </div>

      <Button type="submit" loading={isSubmitting} className="w-full">
        Send Message
      </Button>
    </form>
  )
}''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Manual state management for each field with useState",
            why="Verbose, error-prone, hard to maintain, no validation integration",
            good="Use React Hook Form for automatic state management",
        ),
        AntiPattern(
            bad="Validate only on submit",
            why="Users don't get feedback until they try to submit, frustrating UX",
            good="Validate on blur so users get immediate feedback after interaction",
        ),
        AntiPattern(
            bad="Generic error messages ('Invalid input')",
            why="Users don't know what's wrong or how to fix it",
            good="Specific messages from Zod schema ('Email must include @ symbol')",
        ),
        AntiPattern(
            bad="Not showing loading state during submission",
            why="Users may click submit multiple times, causing duplicate requests",
            good="Show loading spinner and disable button during submission",
        ),
        AntiPattern(
            bad="Ignoring server-side validation errors",
            why="Client-side validation can be bypassed, server errors must be shown",
            good="Use setError to display API validation errors on specific fields",
        ),
        AntiPattern(
            bad="Not resetting form after successful submission",
            why="Confusing UX - form still shows old data, users don't know if it worked",
            good="Call reset() after successful submission to clear form",
        ),
    ]

    file_structure: dict = {
        "components/forms/LoginForm.tsx": "Example login form",
        "components/forms/RegisterForm.tsx": "Example registration form",
        "lib/validations/auth.ts": "Zod schemas for auth forms",
    }

    login_form_code: str = '''// components/forms/LoginForm.tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const loginSchema = z.object({
  email: z.string().email("Please enter a valid email"),
  password: z.string().min(8, "Password must be at least 8 characters"),
})

type LoginFormData = z.infer<typeof loginSchema>

export function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setError,
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    mode: "onBlur",
  })

  const onSubmit = async (data: LoginFormData) => {
    try {
      // Replace with your API call
      const response = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      })

      if (!response.ok) {
        throw new Error("Login failed")
      }

      const result = await response.json()
      // Handle success (e.g., redirect, store token)
      console.log("Login successful:", result)
    } catch (error) {
      setError("root", {
        type: "server",
        message: "Invalid email or password. Please try again.",
      })
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 max-w-md">
      {errors.root && (
        <div className="rounded-lg bg-red-50 border border-red-200 p-4">
          <p className="text-sm text-red-600">{errors.root.message}</p>
        </div>
      )}

      <Input
        label="Email"
        type="email"
        placeholder="you@example.com"
        {...register("email")}
        error={errors.email}
        required
      />

      <Input
        label="Password"
        type="password"
        {...register("password")}
        error={errors.password}
        required
      />

      <Button type="submit" loading={isSubmitting} className="w-full">
        Sign In
      </Button>
    </form>
  )
}
'''

    register_form_code: str = '''// components/forms/RegisterForm.tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const registerSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Please enter a valid email"),
  password: z.string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Password must contain at least one uppercase letter")
    .regex(/[0-9]/, "Password must contain at least one number"),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})

type RegisterFormData = z.infer<typeof registerSchema>

export function RegisterForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
    setError,
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    mode: "onBlur",
  })

  const onSubmit = async (data: RegisterFormData) => {
    try {
      const response = await fetch("/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.message || "Registration failed")
      }

      reset()
      // Show success message (e.g., with toast)
      console.log("Registration successful!")
    } catch (error) {
      setError("root", {
        type: "server",
        message: error instanceof Error ? error.message : "Registration failed. Please try again.",
      })
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 max-w-md">
      {errors.root && (
        <div className="rounded-lg bg-red-50 border border-red-200 p-4">
          <p className="text-sm text-red-600">{errors.root.message}</p>
        </div>
      )}

      <Input
        label="Name"
        {...register("name")}
        error={errors.name}
        required
      />

      <Input
        label="Email"
        type="email"
        placeholder="you@example.com"
        {...register("email")}
        error={errors.email}
        required
      />

      <Input
        label="Password"
        type="password"
        helperText="Must be at least 8 characters with 1 uppercase and 1 number"
        {...register("password")}
        error={errors.password}
        required
      />

      <Input
        label="Confirm Password"
        type="password"
        {...register("confirmPassword")}
        error={errors.confirmPassword}
        required
      />

      <Button type="submit" loading={isSubmitting} className="w-full">
        Create Account
      </Button>
    </form>
  )
}
'''

    validations_code: str = '''// lib/validations/auth.ts
import { z } from "zod"

export const loginSchema = z.object({
  email: z.string().email("Please enter a valid email"),
  password: z.string().min(8, "Password must be at least 8 characters"),
})

export const registerSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Please enter a valid email"),
  password: z.string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Password must contain at least one uppercase letter")
    .regex(/[0-9]/, "Password must contain at least one number"),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})

export type LoginFormData = z.infer<typeof loginSchema>
export type RegisterFormData = z.infer<typeof registerSchema>
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Generate form components and validation schemas.

        Args:
            context: Optional configuration (not used currently)

        Returns:
            Dictionary of filepath: code
        """
        return {
            "components/forms/LoginForm.tsx": self.login_form_code,
            "components/forms/RegisterForm.tsx": self.register_form_code,
            "lib/validations/auth.ts": self.validations_code,
        }
