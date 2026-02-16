"""
Project variant types for VIIPER.

Defines different types of projects with specific characteristics,
timelines, and success metrics.
"""

from enum import Enum
from typing import Dict, Any


class Variant(str, Enum):
    """
    Project variant types with specific characteristics.
    
    Each variant has optimized workflows, agent configurations,
    and success metrics.
    """
    
    LANDING = "landing"  # Landing pages for lead generation
    WEB = "web"          # Content websites, blogs, portfolios
    SAAS = "saas"        # Software as a Service applications
    MOBILE = "mobile"    # Mobile applications (iOS/Android)
    AI = "ai"            # AI/ML products
    PLATFORM = "platform"  # Two-sided marketplaces
    ENTERPRISE = "enterprise"  # B2B enterprise software
    
    def __str__(self) -> str:
        return self.value
    
    @property
    def display_name(self) -> str:
        """Get human-readable display name."""
        names = {
            Variant.LANDING: "Landing Page",
            Variant.WEB: "Website",
            Variant.SAAS: "SaaS Application",
            Variant.MOBILE: "Mobile App",
            Variant.AI: "AI Product",
            Variant.PLATFORM: "Platform/Marketplace",
            Variant.ENTERPRISE: "Enterprise Software"
        }
        return names[self]
    
    @property
    def typical_timeline_weeks(self) -> tuple[int, int]:
        """Get typical timeline range in weeks (min, max)."""
        timelines = {
            Variant.LANDING: (1, 4),
            Variant.WEB: (4, 8),
            Variant.SAAS: (8, 20),
            Variant.MOBILE: (12, 24),
            Variant.AI: (12, 30),
            Variant.PLATFORM: (16, 32),
            Variant.ENTERPRISE: (24, 48)
        }
        return timelines[self]
    
    @property
    def typical_budget_range(self) -> tuple[int, int]:
        """Get typical budget range in EUR (min, max)."""
        budgets = {
            Variant.LANDING: (500, 2000),
            Variant.WEB: (2000, 5000),
            Variant.SAAS: (5000, 15000),
            Variant.MOBILE: (10000, 30000),
            Variant.AI: (10000, 50000),
            Variant.PLATFORM: (20000, 80000),
            Variant.ENTERPRISE: (50000, 200000)
        }
        return budgets[self]
    
    @property
    def requires_authentication(self) -> bool:
        """Does this variant typically require user authentication?"""
        return self in [Variant.SAAS, Variant.MOBILE, Variant.AI, 
                       Variant.PLATFORM, Variant.ENTERPRISE]
    
    @property
    def requires_payments(self) -> bool:
        """Does this variant typically require payment processing?"""
        return self in [Variant.SAAS, Variant.PLATFORM, Variant.ENTERPRISE]
    
    @property
    def primary_metrics(self) -> list[str]:
        """Get primary success metrics for this variant."""
        metrics = {
            Variant.LANDING: ["CTR", "Lead Conversion", "Cost per Lead"],
            Variant.WEB: ["Traffic", "Bounce Rate", "Page Views"],
            Variant.SAAS: ["MRR", "Churn", "LTV/CAC"],
            Variant.MOBILE: ["DAU", "Retention", "In-App Purchases"],
            Variant.AI: ["Accuracy", "Latency", "Cost per Prediction"],
            Variant.PLATFORM: ["GMV", "Take Rate", "Liquidity"],
            Variant.ENTERPRISE: ["ACV", "Sales Cycle", "Expansion Revenue"]
        }
        return metrics[self]
    
    @property
    def recommended_tech_stack(self) -> Dict[str, str]:
        """Get recommended technology stack."""
        stacks = {
            Variant.LANDING: {
                "frontend": "HTML/CSS/JS or Next.js",
                "deployment": "Vercel/Netlify",
                "analytics": "Google Analytics"
            },
            Variant.WEB: {
                "framework": "Next.js or Astro",
                "cms": "Sanity or Contentful",
                "deployment": "Vercel"
            },
            Variant.SAAS: {
                "frontend": "Next.js + Tailwind",
                "backend": "Node.js or Python",
                "database": "PostgreSQL + Supabase",
                "auth": "NextAuth or Supabase Auth",
                "payments": "Stripe"
            },
            Variant.MOBILE: {
                "framework": "React Native or Flutter",
                "backend": "Supabase or Firebase",
                "distribution": "App Store + Play Store"
            },
            Variant.AI: {
                "ml": "PyTorch or TensorFlow",
                "api": "FastAPI",
                "inference": "AWS Lambda or Modal",
                "monitoring": "Weights & Biases"
            },
            Variant.PLATFORM: {
                "frontend": "Next.js",
                "backend": "Node.js",
                "database": "PostgreSQL",
                "matching": "Custom algorithm",
                "payments": "Stripe Connect"
            },
            Variant.ENTERPRISE: {
                "frontend": "React + TypeScript",
                "backend": "Java/C# or Node.js",
                "database": "PostgreSQL or Oracle",
                "auth": "SSO (SAML/OAuth)",
                "compliance": "SOC2, HIPAA ready"
            }
        }
        return stacks[self]
    
    def get_characteristics(self) -> Dict[str, Any]:
        """Get all characteristics for this variant."""
        return {
            "display_name": self.display_name,
            "timeline_weeks": self.typical_timeline_weeks,
            "budget_range": self.typical_budget_range,
            "requires_auth": self.requires_authentication,
            "requires_payments": self.requires_payments,
            "primary_metrics": self.primary_metrics,
            "tech_stack": self.recommended_tech_stack
        }
