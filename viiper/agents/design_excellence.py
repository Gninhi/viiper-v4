"""
Design Excellence Framework for World-Class Applications.

Elevates agent capabilities to produce Awwwards-level design and UX.
"""

from typing import Dict, List, Any
from enum import Enum


class DesignPhilosophy(str, Enum):
    """World-class design philosophies."""

    MINIMALIST_LUXURY = "minimalist_luxury"  # Apple, Stripe
    BOLD_EXPERIMENTAL = "bold_experimental"  # Awwwards winners
    EDITORIAL_STORYTELLING = "editorial_storytelling"  # Medium, Bloomberg
    IMMERSIVE_3D = "immersive_3d"  # Spline, Three.js showcases
    BRUTALIST_MODERN = "brutalist_modern"  # Gumroad, Linear
    KINETIC_TYPOGRAPHY = "kinetic_typography"  # Motion-heavy sites
    SWISS_PRECISION = "swiss_precision"  # Ultra-clean, grid-based


class ColorSystem:
    """
    World-class color system guidelines.

    AVOID: Generic startup colors (purple #7C3AED, blue #3B82F6)
    """

    EXCEPTIONAL_PALETTES = {
        "monochrome_luxury": {
            "description": "Pure black/white with single accent",
            "palette": {
                "primary": "#000000",
                "background": "#FFFFFF",
                "accent": "#FF3366",  # Strategic pop of color
                "text": "#1A1A1A",
                "subtle": "#F5F5F5"
            },
            "inspiration": ["Apple", "Stripe", "Linear"],
            "usage": "Premium products, SaaS, fintech"
        },
        "earth_tones": {
            "description": "Natural, warm, sophisticated",
            "palette": {
                "primary": "#2C2416",  # Deep brown
                "background": "#FAF8F5",  # Warm white
                "accent": "#D4A574",  # Gold/tan
                "text": "#3D3025",
                "subtle": "#E8E3DC"
            },
            "inspiration": ["Kinfolk", "Cereal Magazine"],
            "usage": "Lifestyle, e-commerce, editorial"
        },
        "cyberpunk_noir": {
            "description": "Dark, futuristic, high contrast",
            "palette": {
                "primary": "#0A0E1A",  # Near black navy
                "background": "#050810",  # Deep space
                "accent": "#00FF88",  # Electric mint
                "text": "#E0E7FF",
                "subtle": "#1A1F3A"
            },
            "inspiration": ["Vercel", "Railway", "Raycast"],
            "usage": "Developer tools, AI products, gaming"
        },
        "pastel_brutalism": {
            "description": "Soft colors, hard edges",
            "palette": {
                "primary": "#FFE5E5",  # Soft pink
                "background": "#FFFBF5",  # Cream
                "accent": "#000000",  # Hard black
                "text": "#1A1A1A",
                "subtle": "#F0E6FF"  # Soft lavender
            },
            "inspiration": ["Gumroad", "Cosmos", "Poolside"],
            "usage": "Creative tools, marketplaces, social"
        },
        "premium_gradients": {
            "description": "Sophisticated gradient systems",
            "palette": {
                "gradient_1": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "gradient_2": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
                "gradient_3": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
                "gradient_mesh": "radial-gradient with 4+ colors, low saturation"
            },
            "rules": [
                "Never use default Tailwind gradients",
                "Subtle, low saturation (10-30%)",
                "Mesh gradients for backgrounds",
                "Animated gradients for CTAs"
            ],
            "inspiration": ["Stripe", "Pitch", "Framer"]
        }
    }

    FORBIDDEN_COLORS = [
        "#7C3AED",  # Generic purple
        "#3B82F6",  # Generic blue
        "#10B981",  # Generic green
        "#F59E0B",  # Generic orange
    ]

    @staticmethod
    def get_palette_for_variant(variant: str, philosophy: DesignPhilosophy) -> Dict[str, Any]:
        """Get color palette based on variant and philosophy."""

        mappings = {
            "saas": {
                DesignPhilosophy.MINIMALIST_LUXURY: "monochrome_luxury",
                DesignPhilosophy.BRUTALIST_MODERN: "pastel_brutalism",
                DesignPhilosophy.SWISS_PRECISION: "monochrome_luxury"
            },
            "ai": {
                DesignPhilosophy.IMMERSIVE_3D: "cyberpunk_noir",
                DesignPhilosophy.BOLD_EXPERIMENTAL: "premium_gradients"
            },
            "platform": {
                DesignPhilosophy.EDITORIAL_STORYTELLING: "earth_tones",
                DesignPhilosophy.MINIMALIST_LUXURY: "monochrome_luxury"
            }
        }

        palette_key = mappings.get(variant, {}).get(
            philosophy,
            "monochrome_luxury"  # Default to luxury
        )

        return ColorSystem.EXCEPTIONAL_PALETTES[palette_key]


class TypographySystem:
    """
    World-class typography systems.

    AVOID: Default system fonts, boring sans-serif
    """

    EXCEPTIONAL_TYPEFACES = {
        "editorial_luxury": {
            "display": "PP Editorial New, Canela, Tiempos Headline",
            "body": "ABC Diatype, Suisse Int'l, GT America",
            "mono": "JetBrains Mono, Berkeley Mono",
            "rationale": "Editorial quality, high contrast, luxury feel",
            "scale": {
                "hero": "clamp(4rem, 12vw, 12rem)",  # 64px - 192px
                "h1": "clamp(3rem, 8vw, 6rem)",
                "h2": "clamp(2rem, 5vw, 3.5rem)",
                "body": "clamp(1.125rem, 2vw, 1.25rem)",  # 18-20px
                "caption": "0.875rem"  # 14px
            },
            "usage": ["SaaS", "Platform", "Landing"]
        },
        "tech_precision": {
            "display": "Inter Display, Space Grotesk, Satoshi",
            "body": "Inter, ABC Diatype, Untitled Sans",
            "mono": "JetBrains Mono, Fira Code",
            "rationale": "Technical precision, clear hierarchy",
            "scale": {
                "hero": "clamp(3.5rem, 10vw, 8rem)",
                "h1": "clamp(2.5rem, 6vw, 4.5rem)",
                "h2": "clamp(1.75rem, 4vw, 3rem)",
                "body": "1rem",  # 16px
                "caption": "0.875rem"
            },
            "usage": ["AI", "Developer Tools"]
        },
        "kinetic_display": {
            "display": "Clash Display, Cabinet Grotesk, Sohne Breit",
            "body": "ABC Diatype, Suisse Int'l",
            "mono": "Berkeley Mono",
            "rationale": "Bold, motion-friendly, experimental",
            "scale": {
                "hero": "clamp(5rem, 15vw, 18rem)",  # Massive
                "h1": "clamp(3rem, 10vw, 8rem)",
                "h2": "clamp(2rem, 6vw, 4rem)",
                "body": "1.125rem",
                "caption": "1rem"
            },
            "usage": ["Bold Experimental", "Kinetic"]
        }
    }

    TYPOGRAPHIC_PRINCIPLES = [
        "Use fluid type scales with clamp()",
        "Minimum 1.125rem (18px) for body text",
        "Line height 1.6-1.8 for body, 1.1-1.3 for display",
        "Letter spacing: tighter for headlines (-0.02em), looser for small text (0.02em)",
        "Optical sizing: enable for variable fonts",
        "Never use font-weight 500 or 600 - use 400, 700, 800+",
        "Establish clear type hierarchy (6+ levels)",
        "Use font features: ligatures, alternate glyphs, old-style numerals"
    ]

    @staticmethod
    def get_system(philosophy: DesignPhilosophy) -> Dict[str, Any]:
        """Get typography system for design philosophy."""
        mapping = {
            DesignPhilosophy.MINIMALIST_LUXURY: "editorial_luxury",
            DesignPhilosophy.EDITORIAL_STORYTELLING: "editorial_luxury",
            DesignPhilosophy.BOLD_EXPERIMENTAL: "kinetic_display",
            DesignPhilosophy.KINETIC_TYPOGRAPHY: "kinetic_display",
            DesignPhilosophy.BRUTALIST_MODERN: "tech_precision",
            DesignPhilosophy.SWISS_PRECISION: "tech_precision",
            DesignPhilosophy.IMMERSIVE_3D: "tech_precision"
        }

        system_key = mapping.get(philosophy, "editorial_luxury")
        return TypographySystem.EXCEPTIONAL_TYPEFACES[system_key]


class LayoutSystem:
    """
    World-class layout and spatial design.

    AVOID: Bootstrap grids, generic containers, centered everything
    """

    LAYOUT_PRINCIPLES = {
        "swiss_grid": {
            "description": "Precise, mathematical grid systems",
            "grid": "CSS Grid with 12-16 columns",
            "spacing": "8px base unit, fibonacci sequence (8, 13, 21, 34, 55, 89)",
            "breakpoints": {
                "mobile": "390px",  # iPhone 14
                "tablet": "834px",  # iPad
                "desktop": "1440px",  # Standard
                "wide": "1920px"  # Cinema
            },
            "container": "max-width: 1600px, padding: clamp(1.5rem, 5vw, 8rem)",
            "examples": ["Linear", "Stripe", "Vercel"]
        },
        "editorial_layout": {
            "description": "Magazine-style asymmetric layouts",
            "grid": "CSS Grid with custom templates",
            "spacing": "Large whitespace, 16px base",
            "principles": [
                "Asymmetric balance",
                "Full-bleed images",
                "Text columns max 75ch",
                "Generous leading (line-height 1.8)",
                "Pull quotes and margin notes"
            ],
            "examples": ["Bloomberg", "The Browser", "Works"]
        },
        "immersive_canvas": {
            "description": "Full viewport, scroll-driven experiences",
            "approach": "100vh sections, scroll-triggered animations",
            "spacing": "Viewport-based (vh, vw)",
            "principles": [
                "Fixed positioning for UI",
                "Scroll velocity effects",
                "Parallax with restraint",
                "Smooth scroll with Lenis",
                "Section-based navigation"
            ],
            "examples": ["Apple product pages", "Awwwards winners"]
        }
    }

    SPACING_SCALES = {
        "fibonacci": [8, 13, 21, 34, 55, 89, 144, 233],
        "major_third": [8, 10, 12, 16, 20, 25, 31, 39, 48, 61],
        "golden_ratio": [8, 13, 21, 34, 55, 89, 144]
    }


class AnimationSystem:
    """
    World-class animation and micro-interactions.

    AVOID: Default Tailwind transitions, fade-in-up everywhere
    """

    ANIMATION_PRINCIPLES = [
        "Use GSAP or Framer Motion, never plain CSS for complex animations",
        "Easing: custom cubic-bezier, never linear or ease-in-out",
        "Duration: 400-800ms for UI, 1200-2000ms for storytelling",
        "Stagger: 50-100ms between elements",
        "Respect prefers-reduced-motion",
        "GPU-accelerate: transform and opacity only",
        "60fps target, measure with DevTools"
    ]

    SIGNATURE_EFFECTS = {
        "magnetic_buttons": {
            "description": "Buttons that follow mouse with smooth physics",
            "tech": "Framer Motion + useMotionValue",
            "easing": "spring(300, 30, 10)",
            "example": "https://lusion.co"
        },
        "scroll_reveal": {
            "description": "Elements reveal on scroll with custom easing",
            "tech": "GSAP ScrollTrigger + SplitText",
            "easing": "expo.out",
            "stagger": "0.05s",
            "example": "https://lusion.co, https://activetheory.net"
        },
        "cursor_trail": {
            "description": "Custom cursor with magnetic effect and trailing",
            "tech": "Custom canvas or Framer Motion",
            "blend_mode": "difference or exclusion",
            "example": "https://cuberto.com"
        },
        "text_scramble": {
            "description": "Text that scrambles/glitches into place",
            "tech": "Custom hook with requestAnimationFrame",
            "characters": "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%",
            "example": "https://linear.app"
        },
        "page_transitions": {
            "description": "Smooth page transitions with View Transitions API",
            "tech": "Next.js + View Transitions API polyfill",
            "duration": "600ms",
            "easing": "cubic-bezier(0.65, 0, 0.35, 1)"
        },
        "3d_hover_cards": {
            "description": "Cards that tilt on hover with lighting effects",
            "tech": "React Three Fiber or vanilla CSS 3D transforms",
            "rotation": "max 15deg",
            "example": "https://apple.com"
        }
    }

    CUSTOM_EASINGS = {
        "expo_out": "cubic-bezier(0.16, 1, 0.3, 1)",
        "circ_out": "cubic-bezier(0.075, 0.82, 0.165, 1)",
        "quint_out": "cubic-bezier(0.23, 1, 0.32, 1)",
        "elastic": "cubic-bezier(0.68, -0.55, 0.265, 1.55)",
        "apple": "cubic-bezier(0.28, 0.11, 0.32, 1)"  # Apple's signature
    }


class ComponentLibrary:
    """
    World-class component patterns.

    AVOID: Shadcn/Radix default styles, generic forms
    """

    EXCEPTIONAL_PATTERNS = {
        "hero_section": {
            "bad": "Centered h1 + subtitle + CTA buttons",
            "good": [
                "Full-viewport video/3D background with overlay text",
                "Split-screen: large typography left, visual right",
                "Kinetic typography that animates on load",
                "Gradient mesh background with floating UI",
                "Scroll-triggered reveal with stagger"
            ],
            "examples": {
                "video_hero": "https://lusion.co",
                "split_screen": "https://linear.app",
                "kinetic": "https://resend.com"
            }
        },
        "navigation": {
            "bad": "Centered logo, generic links, blue CTA",
            "good": [
                "Minimal: logo left, links right, hamburger on mobile",
                "Transparent on scroll, solid on scroll down",
                "Mega menu with images and descriptions",
                "Side navigation drawer (Framer style)",
                "Floating nav pill (Apple style)"
            ],
            "features": [
                "Blur background (backdrop-filter: blur(20px))",
                "Subtle border-bottom",
                "Hide on scroll down, show on scroll up",
                "Active indicator with smooth animation",
                "Keyboard navigation"
            ]
        },
        "cards": {
            "bad": "White box, shadow, padding, border-radius:8px",
            "good": [
                "Borderless with subtle hover state",
                "Image fill with gradient overlay",
                "3D tilt on hover",
                "Glassmorphism with backdrop blur",
                "Outlined with hover fill"
            ],
            "hover_states": [
                "Scale: 1.02-1.05, not more",
                "Lift: translateY(-4px) + shadow",
                "Border highlight",
                "Gradient shift",
                "Image scale inside card"
            ]
        },
        "forms": {
            "bad": "Labels above, blue focus ring, generic button",
            "good": [
                "Floating labels (Material style)",
                "Inline labels (Linear style)",
                "Minimal underline style",
                "Large touch targets (min 44px)",
                "Real-time validation with smooth feedback"
            ],
            "validation": [
                "Inline errors below field",
                "Icon indicators (checkmark, warning)",
                "Color-coded but accessible",
                "Haptic feedback on mobile",
                "Submit disabled until valid"
            ]
        },
        "pricing_tables": {
            "bad": "3 columns, feature checkmarks, generic CTAs",
            "good": [
                "Comparison slider (Vercel style)",
                "Interactive toggle (monthly/yearly)",
                "Feature comparison matrix",
                "Highlighted 'Popular' with glow",
                "Bento grid layout (Raycast style)"
            ]
        }
    }


class DesignExcellenceGuide:
    """
    Master guide for world-class design.

    Reference for agents to produce Awwwards-level work.
    """

    GOLDEN_RULES = [
        # Layout & Spacing
        "Generous whitespace is luxury - never cram",
        "Consistent spacing scale - fibonacci or golden ratio",
        "Max 75ch line length for readability",
        "Vertical rhythm - consistent line-height relationships",

        # Typography
        "Display text should be LARGE (4rem+)",
        "Body text minimum 18px (1.125rem)",
        "Never use font-weight 500 or 600",
        "Establish clear hierarchy (6+ levels)",

        # Color
        "Limit palette to 3-4 colors maximum",
        "Use pure black (#000) or near-black (#0A0A0A)",
        "Avoid default gradients - create custom",
        "Strategic use of accent color",

        # Interaction
        "All animations 400-800ms minimum",
        "Custom easing - never linear",
        "Hover states that surprise and delight",
        "Smooth scroll with momentum",

        # Performance
        "Images: WebP/AVIF, next-gen formats",
        "Lazy load below fold",
        "Preload critical fonts",
        "Code split per route",

        # Accessibility
        "4.5:1 contrast minimum",
        "Keyboard navigable",
        "Screen reader tested",
        "Reduced motion respected",

        # Details
        "Perfect pixel alignment",
        "Anti-aliased text (-webkit-font-smoothing)",
        "Consistent border radius (0, 4, 8, 16)",
        "No orphans in headings (text-wrap: balance)"
    ]

    AWWWARDS_CHECKLIST = {
        "design": [
            "Unique visual identity - not template-like",
            "Exceptional typography - premium fonts",
            "Sophisticated color palette - not generic",
            "Strategic use of whitespace",
            "Original imagery - not stock photos",
            "Micro-interactions throughout",
            "Consistent design language"
        ],
        "user_experience": [
            "Intuitive navigation",
            "Clear information hierarchy",
            "Smooth transitions between states",
            "Helpful feedback on actions",
            "Mobile-first responsive",
            "Fast load times (<2s)",
            "Accessibility compliant"
        ],
        "creativity": [
            "Innovative layout approach",
            "Unexpected interactions",
            "Memorable moments",
            "Story-driven design",
            "Bold creative risks",
            "Emotional connection"
        ],
        "code_quality": [
            "Semantic HTML5",
            "Modern CSS (Grid, custom properties)",
            "Performance optimized",
            "SEO optimized",
            "Cross-browser tested",
            "Progressive enhancement"
        ]
    }

    INSPIRATION_SOURCES = {
        "awwwards": "https://www.awwwards.com/websites/",
        "site_inspire": "https://www.siteinspire.com/",
        "lapa_ninja": "https://www.lapa.ninja/",
        "godly": "https://godly.website/",
        "httpster": "https://httpster.net/",
        "behance": "https://www.behance.net/",
        "dribbble": "https://dribbble.com/",
        "land_book": "https://land-book.com/"
    }

    REFERENCE_SITES = {
        "minimalist_luxury": [
            "https://stripe.com",
            "https://linear.app",
            "https://vercel.com",
            "https://pitch.com"
        ],
        "bold_experimental": [
            "https://lusion.co",
            "https://activetheory.net",
            "https://cuberto.com",
            "https://resn.co.nz"
        ],
        "editorial": [
            "https://works.studio",
            "https://the-brandidentity.com",
            "https://www.bloomberg.com/"
        ],
        "immersive_3d": [
            "https://bruno-simon.com",
            "https://www.apple.com/",
            "https://threejs-journey.com/"
        ]
    }

    @staticmethod
    def get_design_system(
        variant: str,
        philosophy: DesignPhilosophy = DesignPhilosophy.MINIMALIST_LUXURY
    ) -> Dict[str, Any]:
        """
        Get complete design system for a project.

        Returns world-class design specifications.
        """

        return {
            "philosophy": philosophy.value,
            "colors": ColorSystem.get_palette_for_variant(variant, philosophy),
            "typography": TypographySystem.get_system(philosophy),
            "layout": LayoutSystem.LAYOUT_PRINCIPLES,
            "animations": AnimationSystem.SIGNATURE_EFFECTS,
            "components": ComponentLibrary.EXCEPTIONAL_PATTERNS,
            "golden_rules": DesignExcellenceGuide.GOLDEN_RULES,
            "awwwards_checklist": DesignExcellenceGuide.AWWWARDS_CHECKLIST,
            "references": DesignExcellenceGuide.REFERENCE_SITES.get(
                philosophy.value.split("_")[0],
                DesignExcellenceGuide.REFERENCE_SITES["minimalist_luxury"]
            )
        }
