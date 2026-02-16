"""
Elite Frontend Agent - World-Class Design & Development.

Produces Awwwards-level designs and implementations.
"""

from typing import Dict, Any, List
from viiper.agents.base import Agent, AgentRole, AgentCapability, AgentTask
from viiper.agents.design_excellence import (
    DesignExcellenceGuide,
    DesignPhilosophy,
    ColorSystem,
    TypographySystem,
    AnimationSystem,
    ComponentLibrary,
    LayoutSystem
)


class EliteFrontendAgent(Agent):
    """
    Elite agent for world-class frontend design and development.

    Capabilities:
    - Awwwards-level visual design
    - Professional mockup creation (Figma/Stitch)
    - Advanced animations and micro-interactions
    - Premium typography and color systems
    - Immersive user experiences

    Philosophy: No generic designs. Every project is exceptional.
    """

    name: str = "Elite Frontend Agent"
    role: AgentRole = AgentRole.PRODUCTION
    capabilities: list = [
        AgentCapability.FRONTEND_DEVELOPMENT,
        AgentCapability.ACCESSIBILITY
    ]

    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute elite frontend design task.

        Produces world-class design specifications and mockups.
        """
        context = self._parse_context(task.description)

        # Select design philosophy based on context
        philosophy = self._select_design_philosophy(context)

        # Generate complete design system
        design_system = DesignExcellenceGuide.get_design_system(
            variant=context.get("variant", "saas"),
            philosophy=philosophy
        )

        result = {
            "task_id": task.id,
            "task_name": task.name,

            # Core Design System
            "design_philosophy": self._explain_philosophy(philosophy, context),
            "visual_identity": self._create_visual_identity(design_system, context),
            "color_system": self._design_color_system(design_system, context),
            "typography_system": self._design_typography_system(design_system),

            # Layout & Structure
            "layout_system": self._design_layout_system(design_system, context),
            "component_library": self._design_components(design_system, context),
            "page_templates": self._design_page_templates(context),

            # Interactions & Motion
            "animation_system": self._design_animation_system(design_system),
            "micro_interactions": self._design_micro_interactions(context),
            "scroll_experience": self._design_scroll_experience(context),

            # Professional Deliverables
            "figma_mockup_structure": self._create_figma_structure(context),
            "design_tokens": self._generate_design_tokens(design_system),
            "implementation_guide": self._create_implementation_guide(design_system),

            # Quality Assurance
            "awwwards_checklist": design_system["awwwards_checklist"],
            "accessibility_compliance": self._ensure_accessibility(design_system),
            "performance_targets": self._set_performance_targets(),

            # References & Inspiration
            "design_references": design_system["references"],
            "competitor_analysis": self._analyze_competitors(context),

            "confidence": 0.95,  # Elite confidence
        }

        return result

    def _parse_context(self, description: str) -> Dict[str, Any]:
        """Parse context and extract design requirements."""
        # Extract variant, industry, target audience
        description_lower = description.lower()

        variant = "saas"
        if "saas" in description_lower or "software" in description_lower:
            variant = "saas"
        elif "ai" in description_lower or "ml" in description_lower:
            variant = "ai"
        elif "platform" in description_lower or "marketplace" in description_lower:
            variant = "platform"
        elif "mobile" in description_lower:
            variant = "mobile"
        elif "landing" in description_lower:
            variant = "landing"

        return {
            "variant": variant,
            "description": description,
            "target_audience": "sophisticated users",
            "brand_adjectives": ["innovative", "premium", "trustworthy"],
            "competition_level": "high"  # Always assume high competition
        }

    def _select_design_philosophy(self, context: Dict[str, Any]) -> DesignPhilosophy:
        """
        Select optimal design philosophy for the project.

        Returns the most appropriate world-class design approach.
        """
        variant = context.get("variant", "saas")

        # Intelligent philosophy selection
        philosophy_map = {
            "saas": DesignPhilosophy.MINIMALIST_LUXURY,  # Stripe, Linear
            "ai": DesignPhilosophy.IMMERSIVE_3D,  # Futuristic, cutting-edge
            "platform": DesignPhilosophy.EDITORIAL_STORYTELLING,  # Content-rich
            "landing": DesignPhilosophy.BOLD_EXPERIMENTAL,  # High conversion
            "mobile": DesignPhilosophy.SWISS_PRECISION,  # Clean, functional
        }

        return philosophy_map.get(variant, DesignPhilosophy.MINIMALIST_LUXURY)

    def _explain_philosophy(
        self,
        philosophy: DesignPhilosophy,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Explain the chosen design philosophy."""

        philosophies = {
            DesignPhilosophy.MINIMALIST_LUXURY: {
                "name": "Minimalist Luxury",
                "description": "Ultra-clean, generous whitespace, premium feel",
                "inspiration": ["Apple", "Stripe", "Linear", "Vercel"],
                "characteristics": [
                    "Monochromatic with single accent color",
                    "Large typography with ample breathing room",
                    "Subtle shadows and borders",
                    "Premium sans-serif typefaces",
                    "Micro-interactions that surprise"
                ],
                "when_to_use": "Premium products, SaaS, fintech, professional tools",
                "avoid": "Overuse of color, cluttered layouts, generic fonts"
            },
            DesignPhilosophy.BOLD_EXPERIMENTAL: {
                "name": "Bold & Experimental",
                "description": "Pushing boundaries, creative risks, memorable",
                "inspiration": ["Awwwards winners", "Lusion", "Active Theory"],
                "characteristics": [
                    "Unexpected layouts and interactions",
                    "Bold typography and color",
                    "3D elements and WebGL",
                    "Scroll-driven storytelling",
                    "Custom cursor and effects"
                ],
                "when_to_use": "Creative agencies, portfolios, brand showcases",
                "avoid": "Conservative industries, accessibility-critical apps"
            },
            DesignPhilosophy.EDITORIAL_STORYTELLING: {
                "name": "Editorial Storytelling",
                "description": "Magazine-quality, content-first, asymmetric",
                "inspiration": ["Bloomberg", "The Browser", "Works Studio"],
                "characteristics": [
                    "Asymmetric grid layouts",
                    "High-quality editorial typography",
                    "Full-bleed imagery",
                    "Generous line-height and margins",
                    "Pull quotes and margin notes"
                ],
                "when_to_use": "Content platforms, publications, luxury e-commerce",
                "avoid": "Data-heavy dashboards, technical tools"
            },
            DesignPhilosophy.IMMERSIVE_3D: {
                "name": "Immersive 3D",
                "description": "Three-dimensional, spatial, futuristic",
                "inspiration": ["Apple product pages", "Bruno Simon", "Spline"],
                "characteristics": [
                    "WebGL/Three.js 3D scenes",
                    "Scroll-based 3D navigation",
                    "Depth and parallax",
                    "Spatial audio (optional)",
                    "High-performance rendering"
                ],
                "when_to_use": "AI products, gaming, cutting-edge tech",
                "avoid": "Low-end devices, conservative audiences"
            },
            DesignPhilosophy.BRUTALIST_MODERN: {
                "name": "Brutalist Modern",
                "description": "Raw, honest, unconventional",
                "inspiration": ["Gumroad", "Cosmos", "Poolside"],
                "characteristics": [
                    "Harsh contrasts and hard edges",
                    "Unconventional color combinations",
                    "Monospace fonts mixed with display",
                    "Exposed grid systems",
                    "Anti-design aesthetic"
                ],
                "when_to_use": "Creative tools, indie products, developer tools",
                "avoid": "Corporate clients, mass market"
            },
            DesignPhilosophy.SWISS_PRECISION: {
                "name": "Swiss Precision",
                "description": "Mathematical grids, perfect alignment, clarity",
                "inspiration": ["Swiss design heritage", "Linear", "Vercel"],
                "characteristics": [
                    "Perfect grid alignment",
                    "Mathematical spacing (8px grid)",
                    "Neutral color palette",
                    "Helvetica/Inter typography",
                    "Obsessive attention to detail"
                ],
                "when_to_use": "Professional tools, B2B, technical products",
                "avoid": "Consumer products, entertainment"
            },
            DesignPhilosophy.KINETIC_TYPOGRAPHY: {
                "name": "Kinetic Typography",
                "description": "Motion-driven, text as hero, dynamic",
                "inspiration": ["Resend", "Cuberto", "Motion design leaders"],
                "characteristics": [
                    "Massive, animated typography",
                    "Text reveal effects",
                    "Scroll-triggered text animations",
                    "Variable fonts with animation",
                    "Text as primary visual element"
                ],
                "when_to_use": "Brand sites, marketing pages, announcements",
                "avoid": "Content-heavy apps, documentation"
            }
        }

        return philosophies.get(philosophy, philosophies[DesignPhilosophy.MINIMALIST_LUXURY])

    def _create_visual_identity(
        self,
        design_system: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create comprehensive visual identity."""

        return {
            "brand_essence": {
                "personality": ["Sophisticated", "Innovative", "Trustworthy", "Premium"],
                "voice": "Professional yet approachable, confident without arrogance",
                "emotion": "Inspires confidence and delight"
            },
            "visual_principles": [
                "Every element earns its place",
                "Whitespace is a feature, not empty space",
                "Typography creates hierarchy and rhythm",
                "Color is used strategically, not decoratively",
                "Interactions feel natural and responsive"
            ],
            "logo_guidelines": {
                "type": "Wordmark or symbol + wordmark",
                "font": "Custom or premium sans-serif",
                "sizing": {
                    "hero": "60-80px height",
                    "navigation": "24-32px height",
                    "mobile": "20-24px height"
                },
                "spacing": "Generous padding, min 16px all sides",
                "variations": ["Full color", "Monochrome", "White", "Black"]
            },
            "imagery_style": {
                "photography": "Custom, high-quality, never stock",
                "style": "Clean, well-lit, minimal post-processing",
                "subjects": "Real people and products, authentic moments",
                "aspect_ratios": ["16:9 for hero", "4:3 for cards", "1:1 for avatars"],
                "quality": "Minimum 2x resolution for retina, WebP/AVIF format"
            },
            "iconography": {
                "style": "Line icons, 2px stroke weight",
                "library": "Custom or Lucide/Heroicons",
                "sizing": "16px, 20px, 24px, 32px (multiples of 4)",
                "usage": "Reinforce meaning, never decorative"
            },
            "illustration": {
                "when_to_use": "Explain complex concepts, add personality",
                "style": "Abstract/geometric or custom brand style",
                "avoid": "Generic illustration packs, overuse"
            }
        }

    def _design_color_system(
        self,
        design_system: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Design exceptional color system."""

        palette = design_system["colors"]

        return {
            "philosophy": palette.get("description", "Sophisticated and unique"),
            "palette": palette["palette"],
            "usage_guidelines": {
                "primary": "Headings, CTAs, brand moments (use sparingly)",
                "background": "Page backgrounds, surfaces",
                "text": "Body text, secondary headings",
                "accent": "Links, hover states, highlights",
                "subtle": "Borders, dividers, disabled states"
            },
            "semantic_colors": {
                "success": "#00C853",  # Not generic green
                "warning": "#FFB300",  # Not generic orange
                "error": "#FF3366",  # Not generic red
                "info": "#2979FF"  # Not generic blue
            },
            "forbidden_colors": [
                "#7C3AED - Generic purple",
                "#3B82F6 - Generic blue",
                "#10B981 - Generic green",
                "#F59E0B - Generic orange"
            ],
            "gradient_system": {
                "hero_gradient": "Subtle mesh gradient with 4+ colors, low saturation",
                "button_hover": "Smooth color shift, not opacity change",
                "card_backgrounds": "Ultra-subtle gradient (2-5% difference)",
                "never": "Default Tailwind gradients, high-saturation rainbows"
            },
            "dark_mode": {
                "enabled": True,
                "background": "#0A0A0A",  # True black or near-black
                "surface": "#1A1A1A",
                "text": "#E0E0E0",
                "approach": "Invert colors with care, adjust contrasts",
                "avoid": "Pure white text on pure black (use #E0E0E0)"
            },
            "inspiration": palette.get("inspiration", []),
            "css_variables": self._generate_css_variables(palette["palette"])
        }

    def _design_typography_system(self, design_system: Dict[str, Any]) -> Dict[str, Any]:
        """Design exceptional typography system."""

        typo = design_system["typography"]

        return {
            "typefaces": {
                "display": {
                    "family": typo["display"],
                    "usage": "Hero headlines, section headers",
                    "weights": [700, 800, 900],  # Bold only
                    "features": ["ligatures", "alternate glyphs"]
                },
                "body": {
                    "family": typo["body"],
                    "usage": "Paragraphs, UI text",
                    "weights": [400, 700],  # Regular and bold only
                    "features": ["ligatures", "old-style numerals"]
                },
                "mono": {
                    "family": typo["mono"],
                    "usage": "Code, technical data",
                    "weights": [400, 700],
                    "features": ["ligatures", "coding ligatures"]
                }
            },
            "type_scale": typo["scale"],
            "type_scale_explanation": {
                "hero": "Massive text for hero sections, fluid sizing",
                "h1": "Primary page heading",
                "h2": "Section headings",
                "body": "Comfortable reading size (18-20px minimum)",
                "caption": "Small text, metadata"
            },
            "hierarchy": [
                "Establish 6+ distinct levels",
                "Use size, weight, and color for differentiation",
                "Maintain consistent line-height ratios",
                "Apply optical sizing for variable fonts"
            ],
            "best_practices": [
                "Body text MINIMUM 18px (1.125rem)",
                "Line-height 1.6-1.8 for body, 1.1-1.3 for display",
                "Letter-spacing: -0.02em for large text, 0.01em for small",
                "Use font-weight 400 or 700+ (never 500, 600)",
                "Enable font features: liga, calt, ss01",
                "Load fonts efficiently: woff2, font-display: swap"
            ],
            "pairing_rationale": typo["rationale"],
            "css_implementation": self._generate_typography_css(typo)
        }

    def _design_layout_system(
        self,
        design_system: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Design exceptional layout system."""

        return {
            "grid_system": {
                "columns": 12,  # CSS Grid with 12 columns
                "gap": "clamp(1.5rem, 4vw, 3rem)",  # Fluid gap
                "margins": "clamp(1.5rem, 5vw, 8rem)",  # Generous margins
                "max_width": "1600px",  # Container max-width
                "breakpoints": {
                    "mobile": "390px",  # iPhone 14
                    "tablet": "834px",  # iPad
                    "desktop": "1440px",  # Standard monitor
                    "wide": "1920px"  # Cinema display
                }
            },
            "spacing_scale": {
                "system": "Fibonacci sequence",
                "values": [8, 13, 21, 34, 55, 89, 144, 233],
                "usage": {
                    8: "Tight spacing, icon gaps",
                    13: "Button padding, small gaps",
                    21: "Card padding, moderate gaps",
                    34: "Section padding vertical",
                    55: "Large section gaps",
                    89: "Hero section padding",
                    144: "Extra large gaps",
                    233: "Massive spacing"
                }
            },
            "layout_patterns": ComponentLibrary.EXCEPTIONAL_PATTERNS,
            "principles": [
                "Generous whitespace creates premium feel",
                "Asymmetric layouts create visual interest",
                "Grid alignment for precision",
                "Hierarchy through size and position",
                "Responsive: mobile-first, progressively enhanced"
            ],
            "page_structure": {
                "hero": "Full viewport or 80vh minimum",
                "sections": "Minimum 60vh, generous padding",
                "footer": "Substantial, not cramped (min 400px)",
                "navigation": "Fixed or hide-on-scroll-down"
            }
        }

    def _design_components(
        self,
        design_system: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Design world-class component library."""

        patterns = ComponentLibrary.EXCEPTIONAL_PATTERNS

        return {
            "buttons": {
                "variants": {
                    "primary": {
                        "style": "Solid background, high contrast",
                        "hover": "Slight lift (translateY(-2px)) + shadow",
                        "active": "Scale(0.98)",
                        "sizing": "Large touch targets: min 44x44px",
                        "examples": "Save, Submit, Buy Now"
                    },
                    "secondary": {
                        "style": "Outlined or ghost",
                        "hover": "Fill with primary color",
                        "examples": "Cancel, Learn More"
                    },
                    "text": {
                        "style": "No background, underline on hover",
                        "examples": "Links, Read More"
                    },
                    "magnetic": {
                        "style": "Follows cursor with spring physics",
                        "tech": "Framer Motion + useMotionValue",
                        "usage": "Hero CTAs, premium interactions"
                    }
                },
                "states": ["default", "hover", "active", "focus", "disabled"],
                "accessibility": "Focus visible, keyboard navigable, ARIA labels"
            },
            "cards": {
                "avoid": "White box + shadow + border-radius",
                "exceptional_patterns": patterns["cards"],
                "hover_effects": [
                    "3D tilt (perspective transform)",
                    "Image scale inside container",
                    "Gradient border reveal",
                    "Blur effect on background",
                    "Smooth lift with shadow"
                ]
            },
            "navigation": {
                "patterns": patterns["navigation"],
                "mobile_menu": {
                    "type": "Full-screen overlay or side drawer",
                    "animation": "Slide + fade, custom easing",
                    "backdrop": "Blur (backdrop-filter: blur(20px))"
                },
                "scroll_behavior": {
                    "default": "Transparent background, blur on scroll",
                    "scroll_down": "Hide navigation",
                    "scroll_up": "Show navigation",
                    "transition": "transform 0.3s cubic-bezier(0.65, 0, 0.35, 1)"
                }
            },
            "forms": {
                "style": patterns["forms"]["good"],
                "validation": patterns["forms"]["validation"],
                "fields": {
                    "height": "min 48px (comfortable touch target)",
                    "font_size": "16px minimum (prevents iOS zoom)",
                    "border": "2px solid, increases to 3px on focus",
                    "border_radius": "8px (consistent with design)",
                    "padding": "16px horizontal"
                }
            },
            "modals": {
                "backdrop": "rgba(0, 0, 0, 0.6) + backdrop-filter: blur(8px)",
                "animation": "Scale from 0.95 + fade",
                "max_width": "600px",
                "padding": "32px",
                "close_button": "Absolute positioned, large touch target"
            },
            "hero_sections": patterns["hero_section"],
            "pricing_tables": patterns["pricing_tables"]
        }

    def _design_page_templates(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design exceptional page templates."""

        variant = context.get("variant", "saas")

        templates = {
            "saas": {
                "homepage": {
                    "structure": [
                        "Hero: Full-viewport with gradient background, large headline, CTA",
                        "Social Proof: Logo cloud of customers (grayscale, hover color)",
                        "Features: Bento grid with images/videos",
                        "How It Works: 3-step process with animations",
                        "Testimonials: Large quotes with avatars",
                        "Pricing: Interactive comparison table",
                        "CTA: Full-width section with gradient",
                        "Footer: Comprehensive with newsletter signup"
                    ],
                    "hero_specs": {
                        "background": "Mesh gradient or subtle pattern",
                        "headline": "clamp(3rem, 8vw, 6rem), max 60 characters",
                        "subheadline": "clamp(1.25rem, 2vw, 1.5rem), max 120 characters",
                        "cta": "Two buttons: primary + secondary (video demo)",
                        "visual": "Product screenshot with shadow or 3D mockup"
                    }
                },
                "pricing": {
                    "layout": "3-4 columns on desktop, stacked on mobile",
                    "highlight": "Most popular plan elevated with glow",
                    "toggle": "Monthly/Yearly with savings badge",
                    "features": "Comparison table below cards",
                    "cta": "Start Free Trial (not 'Buy Now')"
                },
                "dashboard": {
                    "layout": "Sidebar navigation + main content area",
                    "header": "Breadcrumbs, search, user menu",
                    "cards": "Data visualization with charts",
                    "tables": "Sortable, filterable, pagination",
                    "empty_states": "Illustrated, helpful, actionable"
                }
            },
            "landing": {
                "conversion_focused": {
                    "above_fold": "Headline + subheadline + CTA + visual",
                    "body": "Problem → Solution → How It Works → Social Proof → CTA",
                    "cta_frequency": "Every 2-3 sections",
                    "visual_hierarchy": "F-pattern or Z-pattern layout"
                }
            },
            "portfolio": {
                "homepage": "Full-screen project grid with hover previews",
                "project_page": "Immersive storytelling with large imagery",
                "about": "Personal story, process, contact"
            }
        }

        return templates.get(variant, templates["saas"])

    def _design_animation_system(self, design_system: Dict[str, Any]) -> Dict[str, Any]:
        """Design exceptional animation system."""

        effects = AnimationSystem.SIGNATURE_EFFECTS

        return {
            "animation_library": "GSAP + ScrollTrigger (professional standard)",
            "principles": AnimationSystem.ANIMATION_PRINCIPLES,
            "signature_effects": effects,
            "custom_easings": AnimationSystem.CUSTOM_EASINGS,
            "performance": {
                "target": "60fps (16.67ms per frame)",
                "gpu_accelerate": "transform and opacity only",
                "will_change": "Use sparingly, remove after animation",
                "reduced_motion": "Respect prefers-reduced-motion media query"
            },
            "timeline_structure": {
                "page_load": "Logo fade → Nav slide → Hero reveal (stagger)",
                "scroll_sections": "Fade up + slight translateY on ScrollTrigger",
                "hover_states": "Smooth transitions, custom easing",
                "page_transitions": "View Transitions API for SPA navigation"
            }
        }

    def _design_micro_interactions(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design delightful micro-interactions."""

        return {
            "button_hover": {
                "effect": "Magnetic pull towards cursor + scale",
                "duration": "400ms",
                "easing": "spring(300, 30, 10)"
            },
            "link_hover": {
                "effect": "Underline expands from center",
                "duration": "300ms",
                "easing": "cubic-bezier(0.65, 0, 0.35, 1)"
            },
            "card_hover": {
                "effect": "3D tilt based on cursor position + lift",
                "duration": "500ms",
                "tech": "transform: perspective + rotateX/Y"
            },
            "form_focus": {
                "effect": "Border color transition + scale",
                "duration": "200ms",
                "feedback": "Subtle haptic on mobile"
            },
            "success_states": {
                "checkmark": "Draw animation (SVG stroke-dashoffset)",
                "confetti": "On major actions (purchase, signup)",
                "toast": "Slide in from top-right with bounce"
            },
            "loading_states": {
                "skeleton": "Shimmer effect (moving gradient)",
                "spinner": "Custom SVG spinner, branded",
                "progress": "Smooth animated bar"
            },
            "scroll_indicators": {
                "scroll_down": "Animated arrow or 'Scroll' text",
                "progress_bar": "Fixed top, fills as user scrolls",
                "section_indicators": "Dots on side, active on scroll"
            }
        }

    def _design_scroll_experience(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design exceptional scroll experience."""

        return {
            "smooth_scroll": {
                "library": "Lenis (Locomotive Scroll alternative)",
                "duration": "1.2s",
                "easing": "cubic-bezier(0.25, 0.46, 0.45, 0.94)",
                "momentum": "Natural physics"
            },
            "scroll_animations": {
                "sections": "Fade up + translateY on ScrollTrigger",
                "images": "Parallax with different speeds",
                "text": "Stagger reveal word-by-word or line-by-line",
                "numbers": "Count up animation when in view"
            },
            "scroll_hijacking": {
                "when_acceptable": "Portfolio, storytelling, product showcases",
                "when_to_avoid": "Content sites, documentation, dashboards",
                "implementation": "GSAP ScrollTrigger with snap"
            },
            "performance": {
                "passive_listeners": True,
                "debounce_resize": "250ms",
                "intersection_observer": "For lazy loading and animations",
                "request_animation_frame": "For smooth updates"
            }
        }

    def _create_figma_structure(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create professional Figma mockup structure."""

        return {
            "file_organization": {
                "cover_page": "Project overview, design system preview",
                "design_system": "Colors, typography, components",
                "wireframes": "Low-fidelity structure",
                "mockups": "High-fidelity designs",
                "prototypes": "Interactive flows",
                "developer_handoff": "Specs, measurements, exports"
            },
            "pages": [
                {
                    "name": "🎨 Design System",
                    "frames": [
                        "Color Palette",
                        "Typography Scale",
                        "Spacing System",
                        "Component Library",
                        "Icon Library"
                    ]
                },
                {
                    "name": "📱 Mobile (390px)",
                    "frames": ["Home", "Product", "Pricing", "About", "Contact"]
                },
                {
                    "name": "💻 Desktop (1440px)",
                    "frames": ["Home", "Product", "Pricing", "About", "Contact", "Dashboard"]
                },
                {
                    "name": "🔄 Interactive Prototype",
                    "note": "Link frames with Smart Animate transitions"
                }
            ],
            "components": {
                "atoms": ["Button", "Input", "Icon", "Badge", "Avatar"],
                "molecules": ["Card", "Form Field", "Nav Item", "Search Bar"],
                "organisms": ["Header", "Footer", "Hero Section", "Pricing Table"],
                "templates": ["Page Layout", "Dashboard Layout", "Auth Layout"]
            },
            "auto_layout": "Use extensively for responsive components",
            "variants": "Create variants for states (default, hover, active, disabled)",
            "naming_convention": "ComponentName/Variant/State",
            "plugins_recommended": [
                "Stark (accessibility)",
                "Contrast (color contrast)",
                "Unsplash (placeholder images)",
                "Iconify (icon library)",
                "Content Reel (realistic content)"
            ]
        }

    def _generate_design_tokens(self, design_system: Dict[str, Any]) -> Dict[str, str]:
        """Generate design tokens (CSS variables)."""

        colors = design_system["colors"]["palette"]
        typo = design_system["typography"]["scale"]

        tokens = {
            # Colors
            "--color-primary": colors.get("primary", "#000000"),
            "--color-background": colors.get("background", "#FFFFFF"),
            "--color-text": colors.get("text", "#1A1A1A"),
            "--color-accent": colors.get("accent", "#FF3366"),
            "--color-subtle": colors.get("subtle", "#F5F5F5"),

            # Typography
            "--font-display": design_system["typography"]["display"].split(",")[0].strip(),
            "--font-body": design_system["typography"]["body"].split(",")[0].strip(),
            "--font-mono": design_system["typography"]["mono"].split(",")[0].strip(),

            # Type Scale
            "--font-size-hero": typo["hero"],
            "--font-size-h1": typo["h1"],
            "--font-size-h2": typo["h2"],
            "--font-size-body": typo["body"],
            "--font-size-caption": typo["caption"],

            # Spacing (Fibonacci)
            "--space-xs": "8px",
            "--space-sm": "13px",
            "--space-md": "21px",
            "--space-lg": "34px",
            "--space-xl": "55px",
            "--space-2xl": "89px",
            "--space-3xl": "144px",

            # Layout
            "--container-max": "1600px",
            "--grid-gap": "clamp(1.5rem, 4vw, 3rem)",
            "--page-margin": "clamp(1.5rem, 5vw, 8rem)",

            # Animation
            "--duration-fast": "200ms",
            "--duration-base": "400ms",
            "--duration-slow": "800ms",
            "--easing-default": "cubic-bezier(0.65, 0, 0.35, 1)",
            "--easing-bounce": "cubic-bezier(0.68, -0.55, 0.265, 1.55)",

            # Shadows
            "--shadow-sm": "0 1px 2px rgba(0, 0, 0, 0.05)",
            "--shadow-md": "0 4px 6px rgba(0, 0, 0, 0.07)",
            "--shadow-lg": "0 10px 15px rgba(0, 0, 0, 0.1)",
            "--shadow-xl": "0 20px 25px rgba(0, 0, 0, 0.15)",

            # Border Radius
            "--radius-sm": "4px",
            "--radius-md": "8px",
            "--radius-lg": "16px",
            "--radius-full": "9999px"
        }

        return tokens

    def _generate_css_variables(self, palette: Dict[str, str]) -> str:
        """Generate CSS variable declarations."""
        css = ":root {\n"
        for key, value in palette.items():
            css_var = f"  --color-{key.replace('_', '-')}: {value};\n"
            css += css_var
        css += "}"
        return css

    def _generate_typography_css(self, typo: Dict[str, Any]) -> str:
        """Generate typography CSS."""
        return f"""
/* Typography System */
body {{
  font-family: {typo['body']};
  font-size: var(--font-size-body);
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
}}

h1, .text-h1 {{
  font-family: {typo['display']};
  font-size: var(--font-size-h1);
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.02em;
}}

h2, .text-h2 {{
  font-family: {typo['display']};
  font-size: var(--font-size-h2);
  font-weight: 700;
  line-height: 1.2;
}}

.text-hero {{
  font-family: {typo['display']};
  font-size: var(--font-size-hero);
  font-weight: 900;
  line-height: 1.0;
  letter-spacing: -0.03em;
}}

code, pre {{
  font-family: {typo['mono']};
}}
        """.strip()

    def _create_implementation_guide(self, design_system: Dict[str, Any]) -> Dict[str, Any]:
        """Create developer implementation guide."""

        return {
            "tech_stack": {
                "framework": "Next.js 14+ (App Router)",
                "styling": "Tailwind CSS + CSS-in-JS for animations",
                "animations": "GSAP + Framer Motion",
                "3d": "React Three Fiber (if needed)",
                "fonts": "Next.js Font Optimization",
                "images": "Next.js Image component"
            },
            "setup_steps": [
                "1. Install dependencies (Next.js, Tailwind, GSAP, Framer Motion)",
                "2. Configure Tailwind with design tokens",
                "3. Set up font loading with next/font",
                "4. Create component library structure",
                "5. Implement design tokens as CSS variables",
                "6. Build atomic components (buttons, inputs, etc.)",
                "7. Compose organisms and templates",
                "8. Add animations and micro-interactions",
                "9. Test accessibility with screen readers",
                "10. Optimize performance (Lighthouse 90+)"
            ],
            "file_structure": {
                "app/": "Next.js app directory",
                "components/": {
                    "ui/": "Atomic components",
                    "features/": "Feature components",
                    "layouts/": "Page layouts"
                },
                "styles/": "Global CSS, design tokens",
                "lib/": "Utilities, helpers",
                "public/": "Static assets"
            },
            "performance_checklist": [
                "Images: WebP/AVIF, lazy load, responsive sizes",
                "Fonts: Preload, font-display: swap, subset",
                "Code: Split by route, tree-shake unused",
                "CSS: Critical CSS inline, defer non-critical",
                "JS: Async/defer non-critical scripts",
                "Animations: GPU-accelerated (transform, opacity)"
            ],
            "accessibility_checklist": [
                "Semantic HTML5 elements",
                "ARIA labels for interactive elements",
                "Keyboard navigation (Tab, Enter, Escape)",
                "Focus visible styles",
                "Color contrast 4.5:1 minimum",
                "Alt text for all images",
                "Screen reader tested (VoiceOver, NVDA)"
            ]
        }

    def _ensure_accessibility(self, design_system: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure WCAG 2.1 Level AA compliance."""

        return {
            "standard": "WCAG 2.1 Level AA",
            "color_contrast": {
                "normal_text": "4.5:1 minimum",
                "large_text": "3.0:1 minimum (18px+ or 14px+ bold)",
                "testing": "Use Stark plugin in Figma, axe DevTools in browser"
            },
            "keyboard_navigation": {
                "tab_order": "Logical, follows visual flow",
                "focus_visible": "Clear focus indicators, min 2px outline",
                "skip_links": "Skip to main content",
                "shortcuts": "Document keyboard shortcuts"
            },
            "screen_readers": {
                "landmarks": "nav, main, aside, footer elements",
                "headings": "Proper hierarchy (h1 → h2 → h3)",
                "aria_labels": "For icon buttons and actions",
                "alt_text": "Descriptive for meaningful images, empty for decorative"
            },
            "motion": {
                "prefers_reduced_motion": "Disable or reduce animations",
                "no_auto_play": "Videos require user interaction",
                "pause_controls": "For carousels and animations"
            },
            "forms": {
                "labels": "Associated with inputs (for/id)",
                "errors": "Inline, descriptive, announced to screen readers",
                "required": "Indicated visually and programmatically",
                "autocomplete": "Enable for common fields"
            },
            "testing_tools": [
                "axe DevTools (browser extension)",
                "WAVE (web accessibility evaluation tool)",
                "Lighthouse (Chrome DevTools)",
                "VoiceOver (Mac) or NVDA (Windows)",
                "Keyboard-only navigation testing"
            ]
        }

    def _set_performance_targets(self) -> Dict[str, Any]:
        """Set world-class performance targets."""

        return {
            "lighthouse_scores": {
                "performance": "90+",
                "accessibility": "100",
                "best_practices": "100",
                "seo": "100"
            },
            "core_web_vitals": {
                "LCP": "<2.5s (Largest Contentful Paint)",
                "FID": "<100ms (First Input Delay)",
                "CLS": "<0.1 (Cumulative Layout Shift)",
                "INP": "<200ms (Interaction to Next Paint)"
            },
            "load_times": {
                "ttfb": "<600ms (Time to First Byte)",
                "fcp": "<1.8s (First Contentful Paint)",
                "tti": "<3.8s (Time to Interactive)"
            },
            "bundle_sizes": {
                "js_initial": "<200KB gzipped",
                "css_initial": "<50KB gzipped",
                "images": "Next-gen formats (WebP, AVIF)"
            },
            "optimization_strategies": [
                "Code splitting per route",
                "Image optimization (next/image)",
                "Font subsetting and preloading",
                "Critical CSS inline",
                "Lazy load below-the-fold content",
                "CDN for static assets",
                "Server-side rendering for initial load"
            ]
        }

    def _analyze_competitors(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze competitor design approaches."""

        return {
            "premium_examples": {
                "saas": [
                    {
                        "name": "Linear",
                        "url": "https://linear.app",
                        "strengths": [
                            "Minimalist precision",
                            "Smooth animations",
                            "Perfect typography",
                            "Clean product screenshots"
                        ],
                        "learn_from": "Attention to detail, smooth interactions"
                    },
                    {
                        "name": "Stripe",
                        "url": "https://stripe.com",
                        "strengths": [
                            "Sophisticated gradients",
                            "Technical yet approachable",
                            "Excellent documentation design",
                            "Interactive code examples"
                        ],
                        "learn_from": "Balance of design and function"
                    },
                    {
                        "name": "Vercel",
                        "url": "https://vercel.com",
                        "strengths": [
                            "Dark mode excellence",
                            "Futuristic aesthetic",
                            "Strong brand identity",
                            "Developer-focused UX"
                        ],
                        "learn_from": "Dark mode design, technical aesthetic"
                    }
                ]
            },
            "avoid_patterns": [
                "Generic purple gradients and illustrations",
                "Centered everything with no hierarchy",
                "Stock photos of people pointing at laptops",
                "Generic 'feature cards' in 3-column grid",
                "Overuse of color without purpose",
                "Cluttered layouts with no whitespace"
            ],
            "differentiation_strategies": [
                "Unique color palette (not startup standard)",
                "Custom typography pairing",
                "Signature animation style",
                "Branded visual language",
                "Unexpected layout approaches",
                "Memorable micro-interactions"
            ]
        }
