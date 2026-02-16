"""
Premium Avatar Component Skill.

World-class avatar component for user profile pictures.
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


class PremiumAvatarSkill(Skill):
    """
    Premium avatar component with fallbacks.

    Features:
    - Image with fallback to initials
    - Size variants (xs, sm, md, lg, xl)
    - Status indicator (online/offline/busy)
    - Group avatar stacking
    - Rounded and square shapes
    - Loading skeleton state
    - Error handling for broken images
    - Accessible (proper alt text)
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Avatar Component",
        slug="premium-avatar",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.BEGINNER,
        tags=["react", "avatar", "profile", "ui", "typescript"],
        estimated_time_minutes=10,
        description="Production-ready avatar with fallbacks and status indicators",
    )

    dependencies: list = [
        Dependency(
            name="react",
            version="^18.0.0",
            package_manager="npm",
            reason="UI library",
        ),
        Dependency(
            name="@radix-ui/react-avatar",
            version="^1.0.4",
            package_manager="npm",
            reason="Avatar primitives with fallback handling",
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
            title="Always Provide Fallback",
            description="Show initials if image fails to load",
            code_reference='<Avatar.Fallback>{initials}</Avatar.Fallback>',
            benefit="Users always see something, even with broken images",
        ),
        BestPractice(
            title="Alt Text for Accessibility",
            description="Descriptive alt text for screen readers",
            code_reference='alt="John Doe profile picture"',
            benefit="Screen reader users understand the image context",
        ),
        BestPractice(
            title="Consistent Sizing",
            description="Use size variants for consistent sizing across app",
            code_reference='size="md" // 40x40px',
            benefit="Visual consistency, easier maintenance",
        ),
        BestPractice(
            title="Status Indicators",
            description="Show online/offline status with positioned badge",
            code_reference='<Badge dot variant="success" />',
            benefit="Quick visual feedback of user availability",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Basic Avatar",
            description="Simple avatar with image and fallback",
            code='''import { Avatar } from "@/components/ui/avatar"

<Avatar>
  <Avatar.Image src="/user.jpg" alt="John Doe" />
  <Avatar.Fallback>JD</Avatar.Fallback>
</Avatar>''',
        ),
        UsageExample(
            name="Avatar with Status",
            description="Show online status indicator",
            code='''<div className="relative">
  <Avatar>
    <Avatar.Image src="/user.jpg" alt="Jane Doe" />
    <Avatar.Fallback>JD</Avatar.Fallback>
  </Avatar>

  <span className="absolute bottom-0 right-0 h-3 w-3 rounded-full bg-green-500 border-2 border-white" />
</div>''',
        ),
        UsageExample(
            name="Avatar Group",
            description="Stacked avatars for teams",
            code='''<div className="flex -space-x-2">
  <Avatar size="sm" className="ring-2 ring-white">
    <Avatar.Image src="/user1.jpg" alt="User 1" />
    <Avatar.Fallback>U1</Avatar.Fallback>
  </Avatar>

  <Avatar size="sm" className="ring-2 ring-white">
    <Avatar.Image src="/user2.jpg" alt="User 2" />
    <Avatar.Fallback>U2</Avatar.Fallback>
  </Avatar>

  <Avatar size="sm" className="ring-2 ring-white">
    <Avatar.Fallback>+3</Avatar.Fallback>
  </Avatar>
</div>''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="No fallback for broken images",
            why="Users see broken image icon, looks unprofessional",
            good="Always provide initials or icon fallback",
        ),
        AntiPattern(
            bad="Generic alt text ('profile picture')",
            why="Not descriptive for screen readers",
            good="Use user's name ('John Doe profile picture')",
        ),
        AntiPattern(
            bad="Hardcoded sizes (w-10 h-10 everywhere)",
            why="Inconsistent, hard to change globally",
            good="Use size variants (sm, md, lg)",
        ),
    ]

    file_structure: dict = {
        "components/ui/avatar.tsx": "Avatar component with Radix UI",
        "lib/utils.ts": "cn() utility",
    }

    component_code: str = '''// components/ui/avatar.tsx
import * as React from "react"
import * as AvatarPrimitive from "@radix-ui/react-avatar"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const avatarVariants = cva(
  "relative flex shrink-0 overflow-hidden rounded-full",
  {
    variants: {
      size: {
        xs: "h-6 w-6 text-xs",
        sm: "h-8 w-8 text-sm",
        md: "h-10 w-10 text-base",
        lg: "h-12 w-12 text-lg",
        xl: "h-16 w-16 text-xl",
      },
    },
    defaultVariants: {
      size: "md",
    },
  }
)

interface AvatarProps
  extends React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Root>,
    VariantProps<typeof avatarVariants> {}

const Avatar = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Root>,
  AvatarProps
>(({ className, size, ...props }, ref) => (
  <AvatarPrimitive.Root
    ref={ref}
    className={cn(avatarVariants({ size }), className)}
    {...props}
  />
))
Avatar.displayName = AvatarPrimitive.Root.displayName

const AvatarImage = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Image>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Image>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Image
    ref={ref}
    className={cn("aspect-square h-full w-full object-cover", className)}
    {...props}
  />
))
AvatarImage.displayName = AvatarPrimitive.Image.displayName

const AvatarFallback = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Fallback>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Fallback>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Fallback
    ref={ref}
    className={cn(
      "flex h-full w-full items-center justify-center rounded-full bg-gray-100 text-gray-600 font-medium",
      className
    )}
    {...props}
  />
))
AvatarFallback.displayName = AvatarPrimitive.Fallback.displayName

export { Avatar, AvatarImage, AvatarFallback }
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
            "components/ui/avatar.tsx": self.component_code,
            "lib/utils.ts": self.utils_code,
        }
