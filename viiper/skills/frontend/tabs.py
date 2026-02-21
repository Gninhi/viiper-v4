"""
Premium Tabs Component Skill.

World-class tabs component with keyboard navigation and animations.
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


class PremiumTabsSkill(Skill):
    """
    Premium tabs component with accessibility and animations.

    Features:
    - Built on Radix UI Tabs primitives
    - Keyboard navigation (arrow keys, Home, End)
    - Controlled and uncontrolled modes
    - Smooth content transitions
    - Active tab indicator animation
    - Vertical and horizontal orientations
    - Icon support in tab triggers
    - Full ARIA attributes
    - Lazy loading of tab content
    - Mobile-friendly (swipe support via extensions)
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Tabs Component",
        slug="premium-tabs",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.BEGINNER,
        tags=["react", "tabs", "navigation", "ui", "typescript", "radix-ui"],
        estimated_time_minutes=15,
        description="Production-ready tabs component with keyboard navigation and smooth animations",
    )

    dependencies: list = FRONTEND_BASE_DEPS + [
        Dependency(
            name="@radix-ui/react-tabs",
            version="^1.0.4",
            package_manager="npm",
            reason="Accessible tabs primitives",
        ),
    ]

    best_practices: list = [
        BestPractice(
            title="Use Tabs Primitives",
            description="Build on Radix UI Tabs for accessibility",
            code_reference="import * as Tabs from '@radix-ui/react-tabs'",
            benefit="Keyboard navigation, ARIA, focus management handled automatically",
        ),
        BestPractice(
            title="Keyboard Navigation",
            description="Support arrow keys, Home, End for tab navigation",
            code_reference="Radix Tabs handles this automatically",
            benefit="Keyboard users can navigate efficiently without mouse",
        ),
        BestPractice(
            title="Visual Active State",
            description="Clear indication of active tab with underline or background",
            code_reference="data-[state=active]:border-b-2 data-[state=active]:border-black",
            benefit="Users know which tab content they're viewing",
        ),
        BestPractice(
            title="Smooth Transitions",
            description="Animate content changes for polish",
            code_reference="data-[state=active]:animate-in data-[state=active]:fade-in-0",
            benefit="Professional feel, reduces jarring content switches",
        ),
        BestPractice(
            title="Lazy Loading",
            description="Only render active tab content to improve performance",
            code_reference="Conditionally render based on active tab",
            benefit="Faster initial load, better performance with many tabs",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Basic Tabs",
            description="Simple tabs for navigation",
            code='''import { Tabs } from "@/components/ui/tabs"

function ProfileTabs() {
  return (
    <Tabs defaultValue="account">
      <Tabs.List>
        <Tabs.Trigger value="account">Account</Tabs.Trigger>
        <Tabs.Trigger value="password">Password</Tabs.Trigger>
        <Tabs.Trigger value="notifications">Notifications</Tabs.Trigger>
      </Tabs.List>

      <Tabs.Content value="account">
        <h2>Account Settings</h2>
        <p>Manage your account settings here.</p>
      </Tabs.Content>

      <Tabs.Content value="password">
        <h2>Change Password</h2>
        <p>Update your password here.</p>
      </Tabs.Content>

      <Tabs.Content value="notifications">
        <h2>Notification Preferences</h2>
        <p>Manage your notifications here.</p>
      </Tabs.Content>
    </Tabs>
  )
}''',
        ),
        UsageExample(
            name="Controlled Tabs",
            description="Tabs with external state control",
            code='''function ControlledTabs() {
  const [activeTab, setActiveTab] = useState("overview")

  return (
    <div>
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <Tabs.List>
          <Tabs.Trigger value="overview">Overview</Tabs.Trigger>
          <Tabs.Trigger value="analytics">Analytics</Tabs.Trigger>
          <Tabs.Trigger value="reports">Reports</Tabs.Trigger>
        </Tabs.List>

        <Tabs.Content value="overview">
          Overview content
        </Tabs.Content>

        <Tabs.Content value="analytics">
          Analytics content
        </Tabs.Content>

        <Tabs.Content value="reports">
          Reports content
        </Tabs.Content>
      </Tabs>

      <p className="mt-4 text-sm text-gray-600">
        Active tab: {activeTab}
      </p>
    </div>
  )
}''',
        ),
        UsageExample(
            name="Tabs with Icons",
            description="Tabs with icons for better visual hierarchy",
            code='''import { User, Settings, Bell } from "lucide-react"

<Tabs defaultValue="profile">
  <Tabs.List>
    <Tabs.Trigger value="profile">
      <User className="h-4 w-4 mr-2" />
      Profile
    </Tabs.Trigger>

    <Tabs.Trigger value="settings">
      <Settings className="h-4 w-4 mr-2" />
      Settings
    </Tabs.Trigger>

    <Tabs.Trigger value="notifications">
      <Bell className="h-4 w-4 mr-2" />
      Notifications
    </Tabs.Trigger>
  </Tabs.List>

  <Tabs.Content value="profile">Profile content</Tabs.Content>
  <Tabs.Content value="settings">Settings content</Tabs.Content>
  <Tabs.Content value="notifications">Notifications content</Tabs.Content>
</Tabs>''',
        ),
        UsageExample(
            name="Lazy-Loaded Tabs",
            description="Optimize performance with lazy loading",
            code='''function LazyTabs() {
  const [activeTab, setActiveTab] = useState("tab1")

  return (
    <Tabs value={activeTab} onValueChange={setActiveTab}>
      <Tabs.List>
        <Tabs.Trigger value="tab1">Tab 1</Tabs.Trigger>
        <Tabs.Trigger value="tab2">Tab 2</Tabs.Trigger>
        <Tabs.Trigger value="tab3">Tab 3</Tabs.Trigger>
      </Tabs.List>

      {/* Only render active tab content */}
      {activeTab === "tab1" && (
        <Tabs.Content value="tab1">
          <ExpensiveComponent1 />
        </Tabs.Content>
      )}

      {activeTab === "tab2" && (
        <Tabs.Content value="tab2">
          <ExpensiveComponent2 />
        </Tabs.Content>
      )}

      {activeTab === "tab3" && (
        <Tabs.Content value="tab3">
          <ExpensiveComponent3 />
        </Tabs.Content>
      )}
    </Tabs>
  )
}''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Building tabs from scratch with onClick handlers",
            why="Missing keyboard navigation, ARIA attributes, focus management",
            good="Use Radix UI Tabs for built-in accessibility",
        ),
        AntiPattern(
            bad="No visual indication of active tab",
            why="Users can't tell which content they're viewing",
            good="Clear active state with border, background, or underline",
        ),
        AntiPattern(
            bad="Abrupt content switching with no transition",
            why="Jarring, feels unpolished, hard to track what changed",
            good="Smooth fade-in animation for content changes",
        ),
        AntiPattern(
            bad="Too many tabs (8+) in horizontal layout",
            why="Tabs wrap or overflow, hard to scan, poor mobile UX",
            good="Limit to 5-6 tabs or use vertical orientation/dropdown",
        ),
    ]

    file_structure: dict = {
        "components/ui/tabs.tsx": "Tabs component with Radix UI",
        "lib/utils.ts": "cn() utility for class merging",
    }

    component_code: str = '''// components/ui/tabs.tsx
import * as React from "react"
import * as TabsPrimitive from "@radix-ui/react-tabs"
import { cn } from "@/lib/utils"

const Tabs = TabsPrimitive.Root

// Tab List (container for triggers)
const TabsList = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.List>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.List>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.List
    ref={ref}
    className={cn(
      "inline-flex h-11 items-center justify-center rounded-lg bg-gray-100 p-1 text-gray-600",
      className
    )}
    {...props}
  />
))
TabsList.displayName = TabsPrimitive.List.displayName

// Tab Trigger (individual tab button)
const TabsTrigger = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Trigger>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Trigger
    ref={ref}
    className={cn(
      "inline-flex items-center justify-center whitespace-nowrap rounded-md px-4 py-2 text-sm font-medium",
      "transition-all duration-200",
      "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-2",
      "disabled:pointer-events-none disabled:opacity-50",
      // Inactive state
      "text-gray-600 hover:text-gray-900",
      // Active state
      "data-[state=active]:bg-white data-[state=active]:text-gray-900 data-[state=active]:shadow-sm",
      className
    )}
    {...props}
  />
))
TabsTrigger.displayName = TabsPrimitive.Trigger.displayName

// Tab Content
const TabsContent = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Content>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Content
    ref={ref}
    className={cn(
      "mt-4 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-2",
      // Animation
      "data-[state=active]:animate-in data-[state=active]:fade-in-0 data-[state=active]:slide-in-from-bottom-1",
      "data-[state=inactive]:animate-out data-[state=inactive]:fade-out-0 data-[state=inactive]:slide-out-to-top-1",
      className
    )}
    {...props}
  />
))
TabsContent.displayName = TabsPrimitive.Content.displayName

/**
 * Premium tabs component with accessibility.
 *
 * Built on Radix UI Tabs for keyboard navigation and ARIA.
 *
 * @example
 * ```tsx
 * <Tabs defaultValue="tab1">
 *   <Tabs.List>
 *     <Tabs.Trigger value="tab1">Tab 1</Tabs.Trigger>
 *     <Tabs.Trigger value="tab2">Tab 2</Tabs.Trigger>
 *   </Tabs.List>
 *
 *   <Tabs.Content value="tab1">Content 1</Tabs.Content>
 *   <Tabs.Content value="tab2">Content 2</Tabs.Content>
 * </Tabs>
 * ```
 */
export { Tabs, TabsList, TabsTrigger, TabsContent }
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
        Generate premium tabs component files.

        Args:
            context: Optional configuration (not used currently)

        Returns:
            Dictionary of filepath: code
        """
        return {
            "components/ui/tabs.tsx": self.component_code,
            "lib/utils.ts": self.utils_code,
        }
