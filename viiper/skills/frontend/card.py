"""
Premium Card Component Skill.

World-class card component with hover effects following Awwwards standards.
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


class PremiumCardSkill(Skill):
    """
    Premium card component with hover effects and variants.

    Features:
    - Multiple variants (default, bordered, ghost, gradient)
    - Hover effects (lift, glow, tilt, border-pulse)
    - Interactive states (clickable cards as links)
    - Composable API (Header, Body, Footer, Image)
    - Loading skeleton state
    - Responsive design
    - Smooth animations
    - Accessible (proper semantic HTML, ARIA when needed)
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Card Component",
        slug="premium-card",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.BEGINNER,
        tags=["react", "card", "ui", "components", "typescript", "tailwind", "hover"],
        estimated_time_minutes=15,
        description="Premium card component with hover effects and composable API",
    )

    dependencies: list = FRONTEND_BASE_DEPS

    best_practices: list = [
        BestPractice(
            title="Composable Components",
            description="Separate Card.Header, Card.Body, Card.Footer for flexibility",
            code_reference="<Card.Header>, <Card.Body>, <Card.Footer>",
            benefit="Developers can customize layout without complex props",
        ),
        BestPractice(
            title="Subtle Hover Effects",
            description="Use transform and shadow for premium lift effect",
            code_reference="hover:-translate-y-1 hover:shadow-xl",
            benefit="Creates depth and interactivity without being overwhelming",
        ),
        BestPractice(
            title="Clickable Cards as Links",
            description="Make entire card clickable when it links somewhere",
            code_reference='<Card as="a" href="/article">',
            benefit="Larger click target, better UX on mobile",
        ),
        BestPractice(
            title="Loading Skeletons",
            description="Show skeleton while content is loading",
            code_reference="<Card loading />",
            benefit="Better perceived performance, users know content is coming",
        ),
        BestPractice(
            title="Responsive Images",
            description="Use aspect ratios and object-fit for consistent image display",
            code_reference='<img className="aspect-video object-cover" />',
            benefit="Prevents layout shift, consistent card heights",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Basic Card",
            description="Simple card with header, body, and footer",
            code='''import { Card } from "@/components/ui/card"

<Card>
  <Card.Header>
    <Card.Title>Premium Feature</Card.Title>
    <Card.Description>
      Unlock advanced capabilities with our premium plan
    </Card.Description>
  </Card.Header>

  <Card.Body>
    <p>Get access to all features including analytics, priority support, and more.</p>
  </Card.Body>

  <Card.Footer>
    <Button variant="primary">Upgrade Now</Button>
  </Card.Footer>
</Card>''',
        ),
        UsageExample(
            name="Image Card with Hover",
            description="Card with image and lift hover effect",
            code='''<Card hover="lift">
  <Card.Image
    src="/product.jpg"
    alt="Product name"
    className="aspect-video object-cover"
  />

  <Card.Body>
    <Card.Title>Product Name</Card.Title>
    <Card.Description>
      Beautiful product description goes here
    </Card.Description>

    <div className="mt-4 flex items-center justify-between">
      <span className="text-2xl font-bold">$99</span>
      <Button size="sm">Add to Cart</Button>
    </div>
  </Card.Body>
</Card>''',
        ),
        UsageExample(
            name="Clickable Card as Link",
            description="Entire card is a clickable link",
            code='''<Card as="a" href="/blog/article-slug" hover="lift">
  <Card.Image
    src="/article-cover.jpg"
    alt="Article title"
  />

  <Card.Body>
    <div className="flex items-center gap-2 text-sm text-gray-600 mb-2">
      <span>5 min read</span>
      <span>•</span>
      <span>March 15, 2024</span>
    </div>

    <Card.Title>How to Build Amazing UIs</Card.Title>
    <Card.Description>
      Learn the secrets to creating world-class user interfaces
    </Card.Description>
  </Card.Body>
</Card>''',
        ),
        UsageExample(
            name="Loading Skeleton",
            description="Card showing loading state",
            code='''<Card loading>
  <Card.Image className="aspect-video" />
  <Card.Body>
    <Card.Title />
    <Card.Description />
  </Card.Body>
</Card>''',
        ),
        UsageExample(
            name="Gradient Card",
            description="Card with gradient background",
            code='''<Card variant="gradient" className="text-white">
  <Card.Body>
    <Card.Title>Premium Tier</Card.Title>
    <p className="text-lg my-4">Everything you need to scale</p>

    <div className="text-3xl font-bold mb-6">
      $49<span className="text-lg font-normal">/mo</span>
    </div>

    <ul className="space-y-2">
      <li>✓ Unlimited projects</li>
      <li>✓ Advanced analytics</li>
      <li>✓ Priority support</li>
    </ul>

    <Button variant="secondary" className="mt-6 w-full">
      Get Started
    </Button>
  </Card.Body>
</Card>''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Using <div> for clickable cards instead of <a> or <button>",
            why="Not keyboard accessible, no semantic meaning, SEO issues",
            good="Use <a> for links, <button> for actions with proper ARIA",
        ),
        AntiPattern(
            bad="Aggressive hover effects (large scale, bright colors, fast transitions)",
            why="Feels cheap, distracting, not premium, triggers motion sickness",
            good="Subtle lift with shadow change, smooth 200-300ms transitions",
        ),
        AntiPattern(
            bad="Inconsistent card heights in grid",
            why="Looks messy, unprofessional, hard to scan",
            good="Use consistent aspect ratios or CSS Grid auto-rows",
        ),
        AntiPattern(
            bad="No loading state, showing empty cards",
            why="Confusing, looks broken, poor perceived performance",
            good="Show skeleton loading state while fetching data",
        ),
    ]

    file_structure: dict = {
        "components/ui/card.tsx": "Card component with sub-components",
        "lib/utils.ts": "cn() utility for class merging",
    }

    component_code: str = '''// components/ui/card.tsx
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const cardVariants = cva(
  // Base styles - ALWAYS applied
  "rounded-xl overflow-hidden transition-all duration-200",
  {
    variants: {
      variant: {
        // Default: White with border
        default: "bg-white border border-gray-200",

        // Bordered: Emphasis on border
        bordered: "bg-white border-2 border-gray-300",

        // Ghost: Subtle, blends with background
        ghost: "bg-gray-50",

        // Gradient: Premium gradient background
        gradient: "bg-gradient-to-br from-black to-gray-800 text-white border-none",
      },
      hover: {
        // No hover effect
        none: "",

        // Lift: Card lifts up with shadow
        lift: "hover:-translate-y-1 hover:shadow-xl cursor-pointer",

        // Glow: Border glow effect
        glow: "hover:shadow-lg hover:border-gray-400 cursor-pointer",

        // Border pulse: Animate border color
        "border-pulse": "hover:border-black cursor-pointer",
      },
    },
    defaultVariants: {
      variant: "default",
      hover: "none",
    },
  }
)

interface CardProps extends React.HTMLAttributes<HTMLElement>, VariantProps<typeof cardVariants> {
  /** Render as different element (e.g., 'a' for link) */
  as?: React.ElementType

  /** Show loading skeleton */
  loading?: boolean
}

/**
 * Premium card component.
 *
 * @example
 * ```tsx
 * <Card hover="lift">
 *   <Card.Header>
 *     <Card.Title>Title</Card.Title>
 *   </Card.Header>
 *   <Card.Body>Content</Card.Body>
 * </Card>
 * ```
 */
const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant, hover, as: Component = "div", loading, children, ...props }, ref) => {
    if (loading) {
      return (
        <div
          ref={ref}
          className={cn(cardVariants({ variant, hover: "none" }), "animate-pulse", className)}
        >
          {children}
        </div>
      )
    }

    return (
      <Component
        ref={ref}
        className={cn(cardVariants({ variant, hover }), className)}
        {...props}
      >
        {children}
      </Component>
    )
  }
)
Card.displayName = "Card"

// Card Header
const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("flex flex-col gap-2 p-6 pb-4", className)}
      {...props}
    />
  )
)
CardHeader.displayName = "CardHeader"

// Card Title
interface CardTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {
  loading?: boolean
}

const CardTitle = React.forwardRef<HTMLHeadingElement, CardTitleProps>(
  ({ className, loading, children, ...props }, ref) => {
    if (loading) {
      return <div className="h-6 w-3/4 bg-gray-200 rounded" />
    }

    return (
      <h3
        ref={ref}
        className={cn("text-xl font-semibold leading-none", className)}
        {...props}
      >
        {children}
      </h3>
    )
  }
)
CardTitle.displayName = "CardTitle"

// Card Description
interface CardDescriptionProps extends React.HTMLAttributes<HTMLParagraphElement> {
  loading?: boolean
}

const CardDescription = React.forwardRef<HTMLParagraphElement, CardDescriptionProps>(
  ({ className, loading, children, ...props }, ref) => {
    if (loading) {
      return (
        <div className="space-y-2">
          <div className="h-4 w-full bg-gray-200 rounded" />
          <div className="h-4 w-2/3 bg-gray-200 rounded" />
        </div>
      )
    }

    return (
      <p
        ref={ref}
        className={cn("text-sm text-gray-600", className)}
        {...props}
      >
        {children}
      </p>
    )
  }
)
CardDescription.displayName = "CardDescription"

// Card Body
const CardBody = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
  )
)
CardBody.displayName = "CardBody"

// Card Footer
const CardFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("flex items-center gap-3 p-6 pt-0", className)}
      {...props}
    />
  )
)
CardFooter.displayName = "CardFooter"

// Card Image
interface CardImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  loading?: boolean
}

const CardImage = React.forwardRef<HTMLImageElement, CardImageProps>(
  ({ className, loading, alt = "", ...props }, ref) => {
    if (loading) {
      return <div className={cn("w-full bg-gray-200", className)} />
    }

    return (
      <img
        ref={ref}
        alt={alt}
        className={cn("w-full object-cover", className)}
        {...props}
      />
    )
  }
)
CardImage.displayName = "CardImage"

// Export as compound component
export {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardBody,
  CardFooter,
  CardImage,
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
        Generate premium card component files.

        Args:
            context: Optional configuration (not used currently)

        Returns:
            Dictionary of filepath: code
        """
        return {
            "components/ui/card.tsx": self.component_code,
            "lib/utils.ts": self.utils_code,
        }
