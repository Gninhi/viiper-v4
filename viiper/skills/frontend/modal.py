"""
Premium Modal/Dialog Component Skill.

World-class modal component with accessibility and animations.
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


class PremiumModalSkill(Skill):
    """
    Premium modal/dialog component with accessibility.

    Features:
    - Accessible dialog built on Radix UI primitives
    - Size variants (sm, md, lg, xl, full)
    - Smooth animations (fade overlay, slide-up content)
    - Focus trap (keyboard navigation contained)
    - ESC to close
    - Click outside to close (configurable)
    - Scroll lock when open
    - Portal rendering (avoids z-index issues)
    - Full ARIA attributes
    - Composable API (Header, Body, Footer)
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Premium Modal/Dialog Component",
        slug="premium-modal",
        category=SkillCategory.FRONTEND_COMPONENTS,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["react", "modal", "dialog", "ui", "typescript", "tailwind", "radix-ui"],
        estimated_time_minutes=25,
        description="Production-ready modal component with accessibility, animations, and focus management",
    )

    dependencies: list = FRONTEND_BASE_DEPS + [
        Dependency(
            name="@radix-ui/react-dialog",
            version="^1.0.5",
            package_manager="npm",
            reason="Accessible dialog primitives with focus management",
        ),
    ]

    best_practices: list = [
        BestPractice(
            title="Use Dialog Primitives",
            description="Build on accessible primitives like Radix UI Dialog",
            code_reference="import * as Dialog from '@radix-ui/react-dialog'",
            benefit="Focus trap, ESC handling, ARIA attributes handled automatically",
        ),
        BestPractice(
            title="Portal Rendering",
            description="Render modal in a portal to avoid z-index issues",
            code_reference="<Dialog.Portal>",
            benefit="Modal renders at root level, avoiding stacking context problems",
        ),
        BestPractice(
            title="Focus Management",
            description="Auto-focus first interactive element, restore focus on close",
            code_reference="Dialog primitive handles this automatically",
            benefit="Keyboard users stay oriented, no lost focus",
        ),
        BestPractice(
            title="Composable API",
            description="Separate Header, Body, Footer components for flexibility",
            code_reference="<Modal.Header>, <Modal.Body>, <Modal.Footer>",
            benefit="Developers can customize layout without prop drilling",
        ),
        BestPractice(
            title="Controlled State",
            description="Support both controlled and uncontrolled usage",
            code_reference="open={isOpen} onOpenChange={setIsOpen}",
            benefit="Works with external state management or standalone",
        ),
        BestPractice(
            title="Smooth Animations",
            description="Fade overlay, slide-up content for premium feel",
            code_reference="animate-in fade-in slide-in-from-bottom-4",
            benefit="Professional, polished user experience",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Basic Modal",
            description="Simple modal with trigger button",
            code="""import { Modal } from "@/components/ui/modal"
import { Button } from "@/components/ui/button"

function App() {
  return (
    <Modal>
      <Modal.Trigger asChild>
        <Button>Open Modal</Button>
      </Modal.Trigger>

      <Modal.Content>
        <Modal.Header>
          <Modal.Title>Welcome</Modal.Title>
          <Modal.Description>
            This is a premium modal component
          </Modal.Description>
        </Modal.Header>

        <Modal.Body>
          <p>Your content goes here...</p>
        </Modal.Body>

        <Modal.Footer>
          <Modal.Close asChild>
            <Button variant="secondary">Cancel</Button>
          </Modal.Close>
          <Button>Confirm</Button>
        </Modal.Footer>
      </Modal.Content>
    </Modal>
  )
}""",
        ),
        UsageExample(
            name="Controlled Modal",
            description="Modal with external state control",
            code="""const [isOpen, setIsOpen] = useState(false)

<Modal open={isOpen} onOpenChange={setIsOpen}>
  <Modal.Content size="lg">
    <Modal.Header>
      <Modal.Title>Edit Profile</Modal.Title>
    </Modal.Header>

    <Modal.Body>
      <form>
        {/* Form fields */}
      </form>
    </Modal.Body>

    <Modal.Footer>
      <Button onClick={() => setIsOpen(false)}>
        Save Changes
      </Button>
    </Modal.Footer>
  </Modal.Content>
</Modal>""",
        ),
        UsageExample(
            name="Confirmation Dialog",
            description="Alert-style confirmation modal",
            code="""<Modal>
  <Modal.Trigger asChild>
    <Button variant="danger">Delete Account</Button>
  </Modal.Trigger>

  <Modal.Content size="sm">
    <Modal.Header>
      <Modal.Title>Are you sure?</Modal.Title>
      <Modal.Description>
        This action cannot be undone. Your account will be permanently deleted.
      </Modal.Description>
    </Modal.Header>

    <Modal.Footer>
      <Modal.Close asChild>
        <Button variant="ghost">Cancel</Button>
      </Modal.Close>
      <Button variant="danger" onClick={handleDelete}>
        Delete Account
      </Button>
    </Modal.Footer>
  </Modal.Content>
</Modal>""",
        ),
        UsageExample(
            name="Full-Screen Modal",
            description="Full-screen modal for complex forms",
            code="""<Modal>
  <Modal.Trigger asChild>
    <Button>New Project</Button>
  </Modal.Trigger>

  <Modal.Content size="full">
    <Modal.Header>
      <Modal.Title>Create New Project</Modal.Title>
    </Modal.Header>

    <Modal.Body className="overflow-y-auto">
      {/* Long form content */}
    </Modal.Body>

    <Modal.Footer>
      <Button variant="secondary">Save Draft</Button>
      <Button>Create Project</Button>
    </Modal.Footer>
  </Modal.Content>
</Modal>""",
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Building modal from scratch with <div> and manual event handling",
            why="Easy to miss accessibility requirements (focus trap, ESC, ARIA), lots of bugs",
            good="Use accessible primitives like Radix UI Dialog",
        ),
        AntiPattern(
            bad="Rendering modal inline without portal",
            why="Z-index conflicts, modal may be hidden behind other elements",
            good="Always render modals in a portal at root level",
        ),
        AntiPattern(
            bad="No way to close modal with keyboard (only X button)",
            why="Keyboard users get trapped, terrible accessibility",
            good="Support ESC key, focus trap with Radix primitives",
        ),
        AntiPattern(
            bad="Not locking scroll when modal is open",
            why="Background content scrolls, confusing UX, modal feels 'floaty'",
            good="Radix Dialog automatically locks scroll when open",
        ),
        AntiPattern(
            bad="Abrupt open/close with no animation",
            why="Jarring, feels unpolished, users may miss state change",
            good="Smooth fade-in overlay + slide-up content animations",
        ),
    ]

    file_structure: dict = {
        "components/ui/modal.tsx": "Modal component with composable sub-components",
        "lib/utils.ts": "cn() utility for class merging",
    }

    component_code: str = """// components/ui/modal.tsx
import * as React from "react"
import * as DialogPrimitive from "@radix-ui/react-dialog"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"
import { X } from "lucide-react" // or your icon library

const Modal = DialogPrimitive.Root
const ModalTrigger = DialogPrimitive.Trigger
const ModalClose = DialogPrimitive.Close
const ModalPortal = DialogPrimitive.Portal

// Overlay (backdrop)
const ModalOverlay = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      // Base styles
      "fixed inset-0 z-50 bg-black/60 backdrop-blur-sm",
      // Animation
      "data-[state=open]:animate-in data-[state=open]:fade-in-0",
      "data-[state=closed]:animate-out data-[state=closed]:fade-out-0",
      className
    )}
    {...props}
  />
))
ModalOverlay.displayName = "ModalOverlay"

// Content variants
const contentVariants = cva(
  // Base styles - ALWAYS applied
  "fixed left-[50%] top-[50%] z-50 translate-x-[-50%] translate-y-[-50%] bg-white rounded-xl shadow-2xl border border-gray-200 focus:outline-none",
  {
    variants: {
      size: {
        sm: "w-full max-w-sm",
        md: "w-full max-w-md",
        lg: "w-full max-w-lg",
        xl: "w-full max-w-xl",
        "2xl": "w-full max-w-2xl",
        full: "w-[calc(100%-2rem)] h-[calc(100%-2rem)] max-w-none",
      },
    },
    defaultVariants: {
      size: "md",
    },
  }
)

interface ModalContentProps
  extends React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>,
    VariantProps<typeof contentVariants> {}

// Main Content
const ModalContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  ModalContentProps
>(({ className, size, children, ...props }, ref) => (
  <ModalPortal>
    <ModalOverlay />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        contentVariants({ size }),
        // Animation
        "data-[state=open]:animate-in data-[state=open]:fade-in-0 data-[state=open]:slide-in-from-bottom-4 data-[state=open]:duration-300",
        "data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:slide-out-to-bottom-4 data-[state=closed]:duration-200",
        className
      )}
      {...props}
    >
      {children}

      {/* Close button */}
      <DialogPrimitive.Close
        className="absolute right-4 top-4 rounded-lg p-1.5 text-gray-500 hover:bg-gray-100 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 transition-colors"
        aria-label="Close"
      >
        <X className="h-4 w-4" />
      </DialogPrimitive.Close>
    </DialogPrimitive.Content>
  </ModalPortal>
))
ModalContent.displayName = "ModalContent"

// Header
const ModalHeader = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      "flex flex-col gap-2 px-6 pt-6 pb-4 border-b border-gray-100",
      className
    )}
    {...props}
  />
)
ModalHeader.displayName = "ModalHeader"

// Title
const ModalTitle = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Title>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Title
    ref={ref}
    className={cn(
      "text-xl font-semibold text-gray-900 leading-none",
      className
    )}
    {...props}
  />
))
ModalTitle.displayName = "ModalTitle"

// Description
const ModalDescription = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Description>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Description
    ref={ref}
    className={cn("text-sm text-gray-600", className)}
    {...props}
  />
))
ModalDescription.displayName = "ModalDescription"

// Body
const ModalBody = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("px-6 py-4", className)} {...props} />
)
ModalBody.displayName = "ModalBody"

// Footer
const ModalFooter = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      "flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-100",
      className
    )}
    {...props}
  />
)
ModalFooter.displayName = "ModalFooter"

/**
 * Premium modal component with accessibility.
 *
 * Built on Radix UI Dialog primitive for full keyboard navigation,
 * focus management, and ARIA attributes.
 *
 * @example
 * ```tsx
 * <Modal>
 *   <Modal.Trigger asChild>
 *     <Button>Open Modal</Button>
 *   </Modal.Trigger>
 *
 *   <Modal.Content>
 *     <Modal.Header>
 *       <Modal.Title>Title</Modal.Title>
 *       <Modal.Description>Description</Modal.Description>
 *     </Modal.Header>
 *
 *     <Modal.Body>
 *       Content goes here
 *     </Modal.Body>
 *
 *     <Modal.Footer>
 *       <Modal.Close asChild>
 *         <Button variant="secondary">Cancel</Button>
 *       </Modal.Close>
 *       <Button>Confirm</Button>
 *     </Modal.Footer>
 *   </Modal.Content>
 * </Modal>
 * ```
 */
export {
  Modal,
  ModalTrigger,
  ModalContent,
  ModalHeader,
  ModalTitle,
  ModalDescription,
  ModalBody,
  ModalFooter,
  ModalClose,
}
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
        Generate premium modal component files.

        Args:
            context: Optional configuration (not used currently)

        Returns:
            Dictionary of filepath: code
        """
        return {
            "components/ui/modal.tsx": self.component_code,
            "lib/utils.ts": self.utils_code,
        }
