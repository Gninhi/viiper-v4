"""Common dependencies shared across skills.

This module provides shared dependency definitions to avoid duplication
across skill implementations.
"""

from viiper.skills.base import Dependency

# =============================================================================
# FRONTEND DEPENDENCIES
# =============================================================================

FRONTEND_BASE_DEPS = [
    Dependency(
        name="react",
        version="^18.0.0",
        package_manager="npm",
        reason="UI library",
    ),
    Dependency(
        name="@types/react",
        version="^18.0.0",
        package_manager="npm",
        reason="TypeScript types for React",
    ),
    Dependency(
        name="tailwindcss",
        version="^3.4.0",
        package_manager="npm",
        reason="Utility-first CSS framework",
    ),
    Dependency(
        name="class-variance-authority",
        version="^0.7.0",
        package_manager="npm",
        reason="Type-safe variant composition",
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

FRONTEND_FORM_DEPS = [
    *FRONTEND_BASE_DEPS,
    Dependency(
        name="react-hook-form",
        version="^7.50.0",
        package_manager="npm",
        reason="Form state and validation management",
    ),
    Dependency(
        name="zod",
        version="^3.22.0",
        package_manager="npm",
        reason="Schema validation",
    ),
    Dependency(
        name="@hookform/resolvers",
        version="^3.3.0",
        package_manager="npm",
        reason="Zod resolver for React Hook Form",
    ),
]

FRONTEND_RADIX_DEPS = [
    *FRONTEND_BASE_DEPS,
    Dependency(
        name="@radix-ui/react-primitive",
        version="^1.0.0",
        package_manager="npm",
        reason="Radix UI primitives for accessibility",
    ),
]

# =============================================================================
# BACKEND DEPENDENCIES
# =============================================================================

BACKEND_NODE_DEPS = [
    Dependency(
        name="express",
        version="^4.18.0",
        package_manager="npm",
        reason="Web framework for Node.js",
    ),
    Dependency(
        name="@types/express",
        version="^4.17.0",
        package_manager="npm",
        reason="TypeScript types for Express",
    ),
    Dependency(
        name="cors",
        version="^2.8.0",
        package_manager="npm",
        reason="Cross-origin resource sharing",
    ),
    Dependency(
        name="helmet",
        version="^7.0.0",
        package_manager="npm",
        reason="Security headers",
    ),
]

BACKEND_PYTHON_DEPS = [
    Dependency(
        name="fastapi",
        version="^0.109.0",
        package_manager="pip",
        reason="Modern web framework for Python",
    ),
    Dependency(
        name="pydantic",
        version="^2.0.0",
        package_manager="pip",
        reason="Data validation using Python type hints",
    ),
    Dependency(
        name="uvicorn",
        version="^0.27.0",
        package_manager="pip",
        reason="ASGI server",
    ),
]

BACKEND_DATABASE_DEPS = [
    *BACKEND_NODE_DEPS,
    Dependency(
        name="prisma",
        version="^5.0.0",
        package_manager="npm",
        reason="Next-generation ORM",
    ),
    Dependency(
        name="@prisma/client",
        version="^5.0.0",
        package_manager="npm",
        reason="Prisma client for database access",
    ),
]

BACKEND_AUTH_DEPS = [
    *BACKEND_NODE_DEPS,
    Dependency(
        name="jsonwebtoken",
        version="^9.0.0",
        package_manager="npm",
        reason="JWT implementation",
    ),
    Dependency(
        name="bcrypt",
        version="^5.0.0",
        package_manager="npm",
        reason="Password hashing",
    ),
]

BACKEND_VALIDATION_DEPS = [
    Dependency(
        name="zod",
        version="^3.22.0",
        package_manager="npm",
        reason="TypeScript-first schema validation",
    ),
    Dependency(
        name="pydantic",
        version="^2.0.0",
        package_manager="pip",
        reason="Python data validation",
    ),
]

# =============================================================================
# DEVOPS DEPENDENCIES
# =============================================================================

DEVOPS_DOCKER_DEPS = [
    Dependency(
        name="docker",
        version="^24.0.0",
        package_manager="pip",
        reason="Docker SDK for Python",
    ),
]

DEVOPS_MONITORING_DEPS = [
    Dependency(
        name="prometheus-client",
        version="^0.19.0",
        package_manager="pip",
        reason="Prometheus instrumentation",
    ),
    Dependency(
        name="sentry-sdk",
        version="^1.40.0",
        package_manager="pip",
        reason="Error tracking and performance monitoring",
    ),
]

# =============================================================================
# TESTING DEPENDENCIES
# =============================================================================

TESTING_DEPS = [
    Dependency(
        name="vitest",
        version="^1.0.0",
        package_manager="npm",
        reason="Next generation testing framework",
    ),
    Dependency(
        name="@testing-library/react",
        version="^14.0.0",
        package_manager="npm",
        reason="React testing utilities",
    ),
    Dependency(
        name="@testing-library/jest-dom",
        version="^6.0.0",
        package_manager="npm",
        reason="Custom jest matchers",
    ),
    Dependency(
        name="playwright",
        version="^1.40.0",
        package_manager="npm",
        reason="E2E testing",
    ),
]

# =============================================================================
# DATA/ML DEPENDENCIES
# =============================================================================

DATA_PROCESSING_DEPS = [
    Dependency(
        name="pandas",
        version="^2.0.0",
        package_manager="pip",
        reason="Data manipulation and analysis",
    ),
    Dependency(
        name="numpy",
        version="^1.24.0",
        package_manager="pip",
        reason="Numerical computing",
    ),
]

ML_DEPS = [
    *DATA_PROCESSING_DEPS,
    Dependency(
        name="openai",
        version="^1.0.0",
        package_manager="pip",
        reason="OpenAI API client",
    ),
    Dependency(
        name="scikit-learn",
        version="^1.3.0",
        package_manager="pip",
        reason="Machine learning library",
    ),
]
