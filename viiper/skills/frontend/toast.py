"""
Premium Toast Notification Skill.

World-class toast notification system for user feedback.
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


class PremiumToastSkill(Skill):
    """
    Premium toast notification system with React Hot Toast.

    Features:
    - Multiple variants (success, error, warning, info, loading)
    - Auto-dismiss with configurable duration
    - Promise-based loading states
    - Custom icons and styling
    - Position configuration (top/bottom, left/center/right)
    - Stacking and animation
    - Accessible (ARIA live regions)
    - Mobile-friendly
    - Type-safe API
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Toast Notifications",
        slug="premium-toast",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.BEGINNER,
        tags=["react", "toast", "notification", "ui", "typescript", "feedback"],
        estimated_time_minutes=10,
        description="Production-ready toast notification system with react-hot-toast",
    )

    dependencies: list = [
        Dependency(
            name="react",
            version="^18.0.0",
            package_manager="npm",
            reason="UI library",
        ),
        Dependency(
            name="react-hot-toast",
            version="^2.4.1",
            package_manager="npm",
            reason="Lightweight toast notification library",
        ),
    ]

    best_practices: list = [
        BestPractice(
            title="Use Semantic Variants",
            description="Use toast.success, toast.error for different feedback types",
            code_reference='toast.success("Saved!"), toast.error("Failed")',
            benefit="Users quickly understand the outcome with color and icon",
        ),
        BestPractice(
            title="Promise Toasts for Async Operations",
            description="Show loading, success, and error states automatically",
            code_reference="toast.promise(saveData(), { loading, success, error })",
            benefit="Automatic state management, great UX for async operations",
        ),
        BestPractice(
            title="Keep Messages Concise",
            description="Short, actionable messages (< 60 characters)",
            code_reference='toast.success("Profile updated!")',
            benefit="Users can quickly scan and understand the message",
        ),
        BestPractice(
            title="Auto-Dismiss",
            description="Set appropriate duration based on message importance",
            code_reference="toast('Message', { duration: 3000 })",
            benefit="Doesn't clutter UI, users can still dismiss manually",
        ),
        BestPractice(
            title="Position Consistently",
            description="Use consistent position throughout app (top-right recommended)",
            code_reference='position: "top-right"',
            benefit="Users know where to look for feedback",
        ),
        BestPractice(
            title="Accessible Live Regions",
            description="Toast uses ARIA live regions for screen readers",
            code_reference="react-hot-toast handles this automatically",
            benefit="Screen reader users get feedback announcements",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Basic Success Toast",
            description="Show success message after action",
            code='''import toast from "react-hot-toast"

function handleSave() {
  // ... save logic
  toast.success("Changes saved successfully!")
}

<Button onClick={handleSave}>Save</Button>''',
        ),
        UsageExample(
            name="Error Toast",
            description="Show error message when something fails",
            code='''function handleDelete() {
  try {
    await api.deleteItem(id)
    toast.success("Item deleted")
  } catch (error) {
    toast.error("Failed to delete item. Please try again.")
  }
}''',
        ),
        UsageExample(
            name="Promise Toast",
            description="Automatic loading, success, and error states",
            code='''async function handleSubmit(data) {
  const promise = api.createUser(data)

  toast.promise(promise, {
    loading: "Creating user...",
    success: "User created successfully!",
    error: "Failed to create user. Please try again.",
  })

  return promise
}''',
        ),
        UsageExample(
            name="Custom Duration",
            description="Toast with custom auto-dismiss time",
            code='''// Show for 5 seconds instead of default 3
toast("Important message", {
  duration: 5000,
  icon: "⚠️",
})

// Persistent toast (manual dismiss only)
toast("Please review this carefully", {
  duration: Infinity,
})''',
        ),
        UsageExample(
            name="Toast with Action",
            description="Toast with undo/action button",
            code='''function handleDelete(id: string) {
  // Optimistically delete
  deleteItem(id)

  toast((t) => (
    <div className="flex items-center gap-3">
      <span>Item deleted</span>
      <button
        onClick={() => {
          restoreItem(id)
          toast.dismiss(t.id)
          toast.success("Item restored")
        }}
        className="px-2 py-1 bg-white text-black rounded font-medium"
      >
        Undo
      </button>
    </div>
  ))
}''',
        ),
        UsageExample(
            name="Loading Toast",
            description="Show loading state, then update",
            code='''async function handleExport() {
  const toastId = toast.loading("Exporting data...")

  try {
    await api.exportData()
    toast.success("Export complete!", { id: toastId })
  } catch (error) {
    toast.error("Export failed", { id: toastId })
  }
}''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Long, verbose toast messages (> 100 characters)",
            why="Hard to read quickly, takes up too much space, users ignore it",
            good="Keep messages short and actionable (< 60 characters)",
        ),
        AntiPattern(
            bad="Using toasts for critical information or confirmation",
            why="Toasts auto-dismiss and can be missed, use Modal for important decisions",
            good="Use toasts for feedback only, modals for critical actions",
        ),
        AntiPattern(
            bad="Showing multiple toasts simultaneously for same action",
            why="Clutters UI, confusing, looks broken",
            good="Use toast.promise to automatically handle loading → success/error",
        ),
        AntiPattern(
            bad="No visual distinction between success/error/warning",
            why="Users can't tell if action succeeded or failed",
            good="Use semantic variants with distinct colors and icons",
        ),
        AntiPattern(
            bad="Using toasts for every single user action",
            why="Alert fatigue, users start ignoring all toasts, annoying",
            good="Reserve for significant actions, not every click/hover",
        ),
    ]

    file_structure: dict = {
        "lib/toast.ts": "Toast configuration and custom toasts",
        "components/providers/ToastProvider.tsx": "Toast provider component",
    }

    toast_config_code: str = '''// lib/toast.ts
import toast, { Toaster, type ToastOptions } from "react-hot-toast"

/**
 * Default toast configuration
 */
export const defaultToastOptions: ToastOptions = {
  // Position
  position: "top-right",

  // Auto-dismiss after 3 seconds
  duration: 3000,

  // Styling
  style: {
    background: "#fff",
    color: "#000",
    border: "1px solid #e5e7eb",
    padding: "16px",
    borderRadius: "12px",
    fontSize: "14px",
    boxShadow: "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
  },

  // Success styling
  success: {
    style: {
      background: "#f0fdf4",
      border: "1px solid #86efac",
    },
    iconTheme: {
      primary: "#16a34a",
      secondary: "#fff",
    },
  },

  // Error styling
  error: {
    style: {
      background: "#fef2f2",
      border: "1px solid #fca5a5",
    },
    iconTheme: {
      primary: "#dc2626",
      secondary: "#fff",
    },
  },

  // Loading styling
  loading: {
    style: {
      background: "#fffbeb",
      border: "1px solid #fde68a",
    },
  },
}

/**
 * Custom toast functions with better defaults
 */
export const showToast = {
  success: (message: string, options?: ToastOptions) =>
    toast.success(message, { ...defaultToastOptions, ...options }),

  error: (message: string, options?: ToastOptions) =>
    toast.error(message, { ...defaultToastOptions, ...options }),

  loading: (message: string, options?: ToastOptions) =>
    toast.loading(message, { ...defaultToastOptions, ...options }),

  promise: <T,>(
    promise: Promise<T>,
    messages: {
      loading: string
      success: string | ((data: T) => string)
      error: string | ((err: any) => string)
    },
    options?: ToastOptions
  ) =>
    toast.promise(
      promise,
      messages,
      { ...defaultToastOptions, ...options }
    ),

  custom: (message: React.ReactNode, options?: ToastOptions) =>
    toast.custom(message, { ...defaultToastOptions, ...options }),
}

export { Toaster }
export default showToast
'''

    toast_provider_code: str = '''// components/providers/ToastProvider.tsx
"use client" // for Next.js App Router

import { Toaster } from "react-hot-toast"

/**
 * Toast Provider - Add to root layout
 *
 * @example
 * ```tsx
 * // app/layout.tsx or pages/_app.tsx
 * export default function RootLayout({ children }) {
 *   return (
 *     <html>
 *       <body>
 *         <ToastProvider />
 *         {children}
 *       </body>
 *     </html>
 *   )
 * }
 * ```
 */
export function ToastProvider() {
  return (
    <Toaster
      position="top-right"
      reverseOrder={false}
      gutter={8}
      toastOptions={{
        // Default duration
        duration: 3000,

        // Default styling
        style: {
          background: "#fff",
          color: "#000",
          border: "1px solid #e5e7eb",
          padding: "16px",
          borderRadius: "12px",
          fontSize: "14px",
          boxShadow: "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
        },

        // Success
        success: {
          duration: 3000,
          style: {
            background: "#f0fdf4",
            border: "1px solid #86efac",
          },
          iconTheme: {
            primary: "#16a34a",
            secondary: "#fff",
          },
        },

        // Error
        error: {
          duration: 4000, // Slightly longer for errors
          style: {
            background: "#fef2f2",
            border: "1px solid #fca5a5",
          },
          iconTheme: {
            primary: "#dc2626",
            secondary: "#fff",
          },
        },

        // Loading
        loading: {
          style: {
            background: "#fffbeb",
            border: "1px solid #fde68a",
          },
        },
      }}
    />
  )
}
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Generate toast notification files.

        Args:
            context: Optional configuration (not used currently)

        Returns:
            Dictionary of filepath: code
        """
        return {
            "lib/toast.ts": self.toast_config_code,
            "components/providers/ToastProvider.tsx": self.toast_provider_code,
        }
