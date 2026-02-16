"""
Production agents for VIIPER framework.

Specialized agents for Phase P (Production): Frontend, Backend, Testing, and DevOps.
"""

from typing import Dict, Any, List
from viiper.agents.base import Agent, AgentRole, AgentCapability, AgentTask


class FrontendAgent(Agent):
    """
    Agent specialized in frontend development.

    Capabilities:
    - UI component structure and organization
    - State management patterns
    - Responsive design implementation
    - Performance optimization
    - Accessibility compliance
    """

    name: str = "Frontend Agent"
    role: AgentRole = AgentRole.PRODUCTION
    capabilities: list = [AgentCapability.FRONTEND_DEVELOPMENT]

    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute frontend development task.

        Generates:
        - Component architecture
        - State management strategy
        - Styling approach
        - Performance optimizations
        """
        context = self._parse_context(task.description)

        result = {
            "task_id": task.id,
            "task_name": task.name,
            "component_structure": self._design_component_structure(context),
            "state_management": self._recommend_state_management(context),
            "styling_strategy": self._plan_styling_approach(context),
            "routing": self._design_routing(context),
            "performance": self._plan_performance_optimizations(),
            "accessibility": self._plan_accessibility(),
            "code_snippets": self._generate_code_snippets(context),
            "dependencies": self._recommend_dependencies(),
            "confidence": 0.87,
        }

        return result

    def _parse_context(self, description: str) -> Dict[str, Any]:
        """Parse context from task description."""
        return {"app_type": "saas", "complexity": "medium", "target": "web"}

    def _design_component_structure(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design component architecture."""
        return {
            "architecture": "Atomic Design",
            "structure": {
                "atoms": ["Button", "Input", "Label", "Icon", "Badge"],
                "molecules": ["FormField", "SearchBar", "Card", "Modal"],
                "organisms": ["Header", "Sidebar", "Table", "Form"],
                "templates": ["DashboardLayout", "AuthLayout", "SettingsLayout"],
                "pages": ["Dashboard", "Login", "Settings", "UserProfile"],
            },
            "directory_structure": {
                "src/": {
                    "components/": {
                        "ui/": "Reusable UI components (atoms, molecules)",
                        "features/": "Feature-specific components (organisms)",
                        "layouts/": "Page layouts and templates",
                    },
                    "pages/": "Next.js pages",
                    "hooks/": "Custom React hooks",
                    "utils/": "Utility functions",
                    "lib/": "Third-party integrations",
                    "styles/": "Global styles and themes",
                    "types/": "TypeScript type definitions",
                }
            },
            "naming_conventions": {
                "components": "PascalCase (Button.tsx)",
                "hooks": "camelCase with 'use' prefix (useAuth.ts)",
                "utils": "camelCase (formatDate.ts)",
                "constants": "UPPER_SNAKE_CASE",
            },
        }

    def _recommend_state_management(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend state management approach."""
        complexity = context.get("complexity", "medium")

        if complexity == "simple":
            strategy = "React Context API"
            rationale = "Built-in, sufficient for simple apps"
        elif complexity == "medium":
            strategy = "Zustand"
            rationale = "Lightweight, simple API, good DX"
        else:
            strategy = "Redux Toolkit"
            rationale = "Complex state, time-travel debugging needed"

        return {
            "primary_strategy": strategy,
            "rationale": rationale,
            "state_categories": {
                "server_state": {
                    "tool": "React Query (TanStack Query)",
                    "use_for": "API data, caching, background updates",
                },
                "ui_state": {
                    "tool": strategy,
                    "use_for": "Modals, sidebars, theme, user preferences",
                },
                "url_state": {"tool": "Next.js Router", "use_for": "Filters, pagination, tabs"},
                "local_state": {"tool": "useState/useReducer", "use_for": "Form inputs, toggles"},
            },
            "best_practices": [
                "Keep state as local as possible",
                "Lift state only when needed",
                "Use server state for API data (don't duplicate in global store)",
                "Normalize complex state structures",
                "Use TypeScript for type-safe state",
            ],
        }

    def _plan_styling_approach(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Plan styling strategy."""
        return {
            "primary": "Tailwind CSS",
            "rationale": "Utility-first, rapid development, consistent design",
            "setup": {
                "config": "tailwind.config.js with custom theme",
                "plugins": ["@tailwindcss/forms", "@tailwindcss/typography"],
                "dark_mode": "class-based dark mode support",
            },
            "organization": {
                "approach": "Component-scoped classes with shared utilities",
                "custom_classes": "Use @apply for frequently repeated patterns",
                "responsive": "Mobile-first with sm, md, lg, xl breakpoints",
            },
            "design_system": {
                "colors": "Define in tailwind.config.js (primary, secondary, etc.)",
                "spacing": "Use Tailwind's spacing scale (4px base)",
                "typography": "Define font families and scales",
                "components": "Use shadcn/ui or Radix UI for accessible components",
            },
            "alternatives": {
                "CSS_Modules": "If Tailwind too opinionated",
                "Styled_Components": "If prefer CSS-in-JS",
                "Vanilla_CSS": "If very custom design needs",
            },
        }

    def _design_routing(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design routing structure."""
        return {
            "framework": "Next.js App Router",
            "structure": {
                "app/": {
                    "(auth)/": "Auth routes (login, signup) - grouped layout",
                    "(dashboard)/": "Protected dashboard routes",
                    "api/": "API routes",
                    "layout.tsx": "Root layout",
                    "page.tsx": "Home page",
                },
            },
            "route_examples": [
                {"path": "/", "page": "Landing/marketing page"},
                {"path": "/login", "page": "Login page", "layout": "(auth)"},
                {"path": "/dashboard", "page": "Dashboard", "protected": True},
                {"path": "/dashboard/settings", "page": "Settings", "protected": True},
                {"path": "/api/users", "type": "API route"},
            ],
            "protection": {
                "method": "Middleware for route protection",
                "redirect": "Unauthenticated users → /login",
                "implementation": "middleware.ts with auth check",
            },
            "navigation": {
                "component": "Next.js Link component",
                "prefetching": "Automatic prefetch on hover",
                "loading_states": "loading.tsx for suspense boundaries",
            },
        }

    def _plan_performance_optimizations(self) -> Dict[str, List[str]]:
        """Plan performance optimizations."""
        return {
            "code_splitting": [
                "Use dynamic imports for heavy components",
                "Route-based code splitting (automatic with Next.js)",
                "Component lazy loading with React.lazy",
            ],
            "image_optimization": [
                "Use Next.js Image component",
                "WebP format with fallbacks",
                "Lazy loading images below fold",
                "Responsive images with srcset",
            ],
            "bundle_optimization": [
                "Analyze bundle with @next/bundle-analyzer",
                "Tree-shake unused code",
                "Use production builds",
                "Target modern browsers (ES2020+)",
            ],
            "runtime_optimization": [
                "React.memo for expensive components",
                "useMemo/useCallback for expensive computations",
                "Virtualize long lists (react-window)",
                "Debounce search inputs",
            ],
            "caching": [
                "HTTP caching headers",
                "CDN for static assets",
                "Service worker for offline support",
                "React Query for API caching",
            ],
        }

    def _plan_accessibility(self) -> Dict[str, Any]:
        """Plan accessibility compliance."""
        return {
            "standard": "WCAG 2.1 Level AA",
            "key_areas": {
                "semantic_html": [
                    "Use proper heading hierarchy (h1-h6)",
                    "Nav, main, article, aside tags",
                    "Button vs link (actions vs navigation)",
                ],
                "keyboard_navigation": [
                    "All interactive elements focusable",
                    "Logical tab order",
                    "Skip to main content link",
                    "Focus visible styles",
                ],
                "screen_readers": [
                    "ARIA labels for icon buttons",
                    "Alt text for all images",
                    "Form labels properly associated",
                    "Live regions for dynamic content",
                ],
                "color_contrast": [
                    "Minimum 4.5:1 for normal text",
                    "Minimum 3:1 for large text",
                    "Don't rely on color alone",
                ],
            },
            "testing_tools": ["axe DevTools", "WAVE", "Lighthouse", "NVDA/JAWS screen readers"],
            "implementation": [
                "Use accessible component libraries (Radix, Headless UI)",
                "Test with keyboard only",
                "Run automated accessibility tests in CI",
            ],
        }

    def _generate_code_snippets(self, context: Dict[str, Any]) -> Dict[str, str]:
        """Generate example code snippets."""
        return {
            "component_example": '''// components/ui/Button.tsx
import { ButtonHTMLAttributes, forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          'rounded font-medium transition-colors',
          {
            'bg-blue-600 text-white hover:bg-blue-700': variant === 'primary',
            'bg-gray-200 text-gray-900 hover:bg-gray-300': variant === 'secondary',
          },
          {
            'px-3 py-1.5 text-sm': size === 'sm',
            'px-4 py-2': size === 'md',
            'px-6 py-3 text-lg': size === 'lg',
          },
          className
        )}
        {...props}
      />
    )
  }
)''',
            "hook_example": '''// hooks/useAuth.ts
import { useSession } from 'next-auth/react'

export function useAuth() {
  const { data: session, status } = useSession()

  return {
    user: session?.user,
    isLoading: status === 'loading',
    isAuthenticated: status === 'authenticated',
  }
}''',
            "api_call_example": '''// hooks/useUsers.ts
import { useQuery } from '@tanstack/react-query'

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const res = await fetch('/api/users')
      if (!res.ok) throw new Error('Failed to fetch users')
      return res.json()
    },
  })
}''',
        }

    def _recommend_dependencies(self) -> Dict[str, List[str]]:
        """Recommend frontend dependencies."""
        return {
            "core": ["next@14", "react@18", "react-dom@18", "typescript@5"],
            "ui": [
                "tailwindcss@3",
                "@radix-ui/react-*",
                "lucide-react (icons)",
                "class-variance-authority",
            ],
            "state": ["zustand@4", "@tanstack/react-query@5"],
            "forms": ["react-hook-form@7", "zod@3"],
            "utils": ["date-fns", "clsx", "tailwind-merge"],
            "dev": ["@next/bundle-analyzer", "eslint", "prettier"],
        }


class BackendAgent(Agent):
    """
    Agent specialized in backend development.

    Capabilities:
    - API design and implementation
    - Database schema design
    - Business logic architecture
    - Authentication and authorization
    - Integration patterns
    """

    name: str = "Backend Agent"
    role: AgentRole = AgentRole.PRODUCTION
    capabilities: list = [AgentCapability.BACKEND_DEVELOPMENT, AgentCapability.DATABASE_DESIGN]

    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute backend development task.

        Generates:
        - API design
        - Database schema
        - Business logic structure
        - Integration patterns
        """
        context = self._parse_context(task.description)

        result = {
            "task_id": task.id,
            "task_name": task.name,
            "api_design": self._design_api(context),
            "database_schema": self._design_database_schema(context),
            "architecture": self._design_backend_architecture(context),
            "authentication": self._design_authentication(),
            "business_logic": self._structure_business_logic(),
            "error_handling": self._plan_error_handling(),
            "code_snippets": self._generate_code_snippets(context),
            "dependencies": self._recommend_dependencies(),
            "confidence": 0.89,
        }

        return result

    def _parse_context(self, description: str) -> Dict[str, Any]:
        """Parse context from task description."""
        return {"app_type": "saas", "scale": "medium", "features": ["auth", "crud", "payments"]}

    def _design_api(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design API structure."""
        return {
            "style": "RESTful",
            "base_url": "/api/v1",
            "endpoints": [
                {
                    "path": "/auth/login",
                    "method": "POST",
                    "description": "User login",
                    "request": {"email": "string", "password": "string"},
                    "response": {"token": "string", "user": "object"},
                },
                {
                    "path": "/users",
                    "method": "GET",
                    "description": "List users",
                    "auth": "required",
                    "query": {"page": "number", "limit": "number"},
                },
                {
                    "path": "/users/:id",
                    "method": "GET",
                    "description": "Get user by ID",
                    "auth": "required",
                },
                {
                    "path": "/users",
                    "method": "POST",
                    "description": "Create user",
                    "auth": "admin",
                    "request": {"email": "string", "name": "string", "role": "string"},
                },
                {
                    "path": "/users/:id",
                    "method": "PUT",
                    "description": "Update user",
                    "auth": "required (own or admin)",
                },
                {
                    "path": "/users/:id",
                    "method": "DELETE",
                    "description": "Delete user",
                    "auth": "admin",
                },
            ],
            "conventions": {
                "naming": "Lowercase, plural nouns (users, posts)",
                "versioning": "URL-based (/api/v1/)",
                "pagination": "?page=1&limit=20",
                "filtering": "?status=active&role=admin",
                "sorting": "?sort=created_at:desc",
            },
            "response_format": {
                "success": {"data": "...", "meta": {"page": 1, "total": 100}},
                "error": {"error": {"code": "USER_NOT_FOUND", "message": "...", "details": "..."}},
            },
        }

    def _design_database_schema(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design database schema."""
        return {
            "database": "PostgreSQL",
            "orm": "Prisma",
            "tables": {
                "users": {
                    "columns": {
                        "id": "UUID PRIMARY KEY",
                        "email": "VARCHAR(255) UNIQUE NOT NULL",
                        "password_hash": "VARCHAR(255) NOT NULL",
                        "name": "VARCHAR(255)",
                        "role": "ENUM('user', 'admin') DEFAULT 'user'",
                        "created_at": "TIMESTAMP DEFAULT NOW()",
                        "updated_at": "TIMESTAMP DEFAULT NOW()",
                    },
                    "indexes": ["email", "created_at"],
                },
                "sessions": {
                    "columns": {
                        "id": "UUID PRIMARY KEY",
                        "user_id": "UUID REFERENCES users(id) ON DELETE CASCADE",
                        "token": "VARCHAR(255) UNIQUE NOT NULL",
                        "expires_at": "TIMESTAMP NOT NULL",
                        "created_at": "TIMESTAMP DEFAULT NOW()",
                    },
                    "indexes": ["token", "user_id", "expires_at"],
                },
                "projects": {
                    "columns": {
                        "id": "UUID PRIMARY KEY",
                        "user_id": "UUID REFERENCES users(id) ON DELETE CASCADE",
                        "name": "VARCHAR(255) NOT NULL",
                        "description": "TEXT",
                        "status": "ENUM('active', 'archived') DEFAULT 'active'",
                        "created_at": "TIMESTAMP DEFAULT NOW()",
                        "updated_at": "TIMESTAMP DEFAULT NOW()",
                    },
                    "indexes": ["user_id", "status", "created_at"],
                },
            },
            "relationships": [
                "users → sessions (one-to-many)",
                "users → projects (one-to-many)",
            ],
            "migrations": {
                "tool": "Prisma Migrate",
                "strategy": "Version-controlled SQL migrations",
                "workflow": "prisma migrate dev → prisma migrate deploy",
            },
        }

    def _design_backend_architecture(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design backend architecture."""
        return {
            "pattern": "Layered Architecture",
            "layers": {
                "routes": "HTTP request handling (Next.js API routes)",
                "controllers": "Request validation, response formatting",
                "services": "Business logic",
                "repositories": "Data access",
                "models": "Domain entities",
            },
            "directory_structure": {
                "app/api/": {
                    "auth/": "Authentication endpoints",
                    "users/": "User CRUD endpoints",
                    "projects/": "Project endpoints",
                },
                "lib/": {
                    "db/": "Database connection and Prisma client",
                    "services/": "Business logic services",
                    "repositories/": "Data access layer",
                    "utils/": "Utility functions",
                    "middleware/": "Auth, logging, etc.",
                },
            },
            "best_practices": [
                "Dependency injection for testability",
                "Single Responsibility Principle per service",
                "Repository pattern for data access",
                "DTO (Data Transfer Objects) for API contracts",
                "Validate inputs with Zod schemas",
            ],
        }

    def _design_authentication(self) -> Dict[str, Any]:
        """Design authentication system."""
        return {
            "strategy": "JWT with refresh tokens",
            "implementation": {
                "library": "NextAuth.js or custom JWT",
                "password_hashing": "bcrypt (cost factor 12)",
                "token_storage": "httpOnly cookies",
                "refresh_strategy": "Sliding window (refresh on use)",
            },
            "flow": {
                "login": [
                    "Validate email/password",
                    "Check user exists and password matches",
                    "Generate access token (15min expiry)",
                    "Generate refresh token (7 days expiry)",
                    "Store tokens in httpOnly cookies",
                    "Return user data",
                ],
                "api_request": [
                    "Extract token from cookie/header",
                    "Verify JWT signature",
                    "Check expiry",
                    "Attach user to request context",
                ],
                "refresh": ["Validate refresh token", "Generate new access token", "Return new tokens"],
            },
            "authorization": {
                "method": "Role-Based Access Control (RBAC)",
                "roles": ["user", "admin"],
                "implementation": "Middleware checks user.role",
            },
        }

    def _structure_business_logic(self) -> Dict[str, Any]:
        """Structure business logic layer."""
        return {
            "pattern": "Service Layer",
            "example_service": {
                "UserService": {
                    "responsibilities": [
                        "User creation and validation",
                        "Password reset workflow",
                        "User profile updates",
                        "User deletion with cleanup",
                    ],
                    "methods": [
                        "createUser(data)",
                        "getUserById(id)",
                        "updateUser(id, data)",
                        "deleteUser(id)",
                        "requestPasswordReset(email)",
                    ],
                }
            },
            "guidelines": [
                "One service per domain entity",
                "Services use repositories for data access",
                "Services contain all business rules",
                "Services throw domain-specific exceptions",
                "Services are transaction boundaries",
            ],
        }

    def _plan_error_handling(self) -> Dict[str, Any]:
        """Plan error handling strategy."""
        return {
            "error_types": {
                "ValidationError": {"status": 400, "example": "Invalid email format"},
                "UnauthorizedError": {"status": 401, "example": "Invalid credentials"},
                "ForbiddenError": {"status": 403, "example": "Insufficient permissions"},
                "NotFoundError": {"status": 404, "example": "User not found"},
                "ConflictError": {"status": 409, "example": "Email already exists"},
                "InternalServerError": {"status": 500, "example": "Database connection failed"},
            },
            "handling_strategy": {
                "validation": "Zod schemas at API boundary",
                "business_logic": "Custom domain exceptions",
                "database": "Catch and transform Prisma errors",
                "unexpected": "Global error handler catches all",
            },
            "response_format": {
                "code": "ERROR_CODE (uppercase snake_case)",
                "message": "User-friendly message",
                "details": "Additional context (dev mode only)",
                "timestamp": "ISO 8601 timestamp",
            },
            "logging": {
                "tool": "Pino or Winston",
                "levels": "error, warn, info, debug",
                "include": "Request ID, user ID, stack trace (errors)",
            },
        }

    def _generate_code_snippets(self, context: Dict[str, Any]) -> Dict[str, str]:
        """Generate backend code snippets."""
        return {
            "api_route": '''// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'
import { UserService } from '@/lib/services/user-service'

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
  password: z.string().min(8),
})

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const data = createUserSchema.parse(body)

    const user = await UserService.createUser(data)

    return NextResponse.json({ data: user }, { status: 201 })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: { code: 'VALIDATION_ERROR', message: 'Invalid input' } },
        { status: 400 }
      )
    }
    // Handle other errors...
  }
}''',
            "service": '''// lib/services/user-service.ts
import { prisma } from '@/lib/db'
import bcrypt from 'bcryptjs'

export class UserService {
  static async createUser(data: { email: string; name: string; password: string }) {
    // Check if user exists
    const existing = await prisma.user.findUnique({
      where: { email: data.email }
    })

    if (existing) {
      throw new ConflictError('Email already registered')
    }

    // Hash password
    const password_hash = await bcrypt.hash(data.password, 12)

    // Create user
    const user = await prisma.user.create({
      data: {
        email: data.email,
        name: data.name,
        password_hash,
      },
      select: {
        id: true,
        email: true,
        name: true,
        created_at: true,
      }
    })

    return user
  }
}''',
        }

    def _recommend_dependencies(self) -> Dict[str, List[str]]:
        """Recommend backend dependencies."""
        return {
            "database": ["@prisma/client@5", "prisma@5 (dev)"],
            "validation": ["zod@3"],
            "auth": ["bcryptjs@2", "jsonwebtoken@9", "next-auth@4"],
            "utils": ["date-fns@2"],
            "dev": ["prisma@5", "@types/bcryptjs", "@types/jsonwebtoken"],
        }


class TestingAgent(Agent):
    """
    Agent specialized in testing and quality assurance.

    Capabilities:
    - Test strategy design
    - Test code generation
    - Coverage analysis
    - CI/CD integration
    """

    name: str = "Testing Agent"
    role: AgentRole = AgentRole.PRODUCTION
    capabilities: list = [AgentCapability.TESTING]

    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute testing task.

        Generates:
        - Test strategy
        - Test suites structure
        - Coverage targets
        - CI/CD integration plan
        """
        context = self._parse_context(task.description)

        result = {
            "task_id": task.id,
            "task_name": task.name,
            "strategy": self._design_test_strategy(),
            "test_suites": self._structure_test_suites(context),
            "coverage_targets": self._set_coverage_targets(),
            "ci_integration": self._plan_ci_integration(),
            "tools": self._recommend_testing_tools(),
            "code_snippets": self._generate_test_examples(),
            "confidence": 0.86,
        }

        return result

    def _parse_context(self, description: str) -> Dict[str, Any]:
        """Parse context."""
        return {"app_type": "saas", "complexity": "medium"}

    def _design_test_strategy(self) -> Dict[str, Any]:
        """Design testing strategy."""
        return {
            "pyramid": {
                "unit_tests": {"percentage": 70, "description": "Functions, hooks, utilities"},
                "integration_tests": {
                    "percentage": 20,
                    "description": "API routes, database operations",
                },
                "e2e_tests": {"percentage": 10, "description": "Critical user flows"},
            },
            "approaches": {
                "unit": "Vitest for fast, isolated tests",
                "integration": "Vitest with test database",
                "e2e": "Playwright for browser automation",
                "visual": "Chromatic or Percy for visual regression",
            },
            "principles": [
                "Test behavior, not implementation",
                "AAA pattern (Arrange, Act, Assert)",
                "One assertion per test (when possible)",
                "Descriptive test names",
                "Avoid test interdependencies",
            ],
        }

    def _structure_test_suites(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Structure test suites."""
        return {
            "directory_structure": {
                "tests/": {
                    "unit/": "Component and function tests",
                    "integration/": "API and database tests",
                    "e2e/": "End-to-end browser tests",
                    "fixtures/": "Test data and mocks",
                },
            },
            "suites": {
                "unit": [
                    "components/*.test.tsx",
                    "hooks/*.test.ts",
                    "utils/*.test.ts",
                    "lib/services/*.test.ts",
                ],
                "integration": ["app/api/**/*.test.ts"],
                "e2e": ["tests/e2e/*.spec.ts"],
            },
            "naming": {
                "files": "*.test.ts or *.spec.ts",
                "tests": "describe('Component') > it('should do something')",
            },
        }

    def _set_coverage_targets(self) -> Dict[str, Any]:
        """Set code coverage targets."""
        return {
            "targets": {
                "overall": "80%",
                "statements": "80%",
                "branches": "75%",
                "functions": "80%",
                "lines": "80%",
            },
            "critical_paths": {
                "authentication": "100%",
                "payment_processing": "100%",
                "data_mutations": "90%",
                "api_routes": "85%",
            },
            "exclusions": [
                "config files",
                "type definitions",
                "dev tooling",
                "generated code",
            ],
        }

    def _plan_ci_integration(self) -> Dict[str, Any]:
        """Plan CI/CD integration."""
        return {
            "workflow": "GitHub Actions",
            "pipeline_stages": {
                "1_lint": "ESLint + Prettier check",
                "2_type_check": "TypeScript compilation",
                "3_unit_tests": "Run Vitest tests",
                "4_integration_tests": "API tests with test DB",
                "5_e2e_tests": "Playwright (on main branch only)",
                "6_coverage": "Upload to Codecov",
            },
            "triggers": {
                "on_pr": "All stages except E2E",
                "on_main": "All stages including E2E",
                "scheduled": "Nightly full test suite",
            },
            "optimizations": [
                "Cache dependencies (node_modules)",
                "Parallel test execution",
                "Skip E2E on docs-only changes",
                "Fail fast on lint errors",
            ],
        }

    def _recommend_testing_tools(self) -> Dict[str, Any]:
        """Recommend testing tools."""
        return {
            "test_runners": {
                "vitest": "Unit and integration tests (fast, Vite-powered)",
                "playwright": "E2E tests (cross-browser)",
            },
            "utilities": {
                "@testing-library/react": "React component testing",
                "@testing-library/user-event": "Simulate user interactions",
                "msw": "Mock Service Worker for API mocking",
            },
            "coverage": {"c8": "Built into Vitest", "codecov": "Coverage reporting"},
            "visual": {"chromatic": "Visual regression testing (Storybook)"},
        }

    def _generate_test_examples(self) -> Dict[str, str]:
        """Generate test code examples."""
        return {
            "component_test": '''// components/Button.test.tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Button } from './Button'

describe('Button', () => {
  it('should render with text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('should call onClick when clicked', async () => {
    const onClick = vi.fn()
    render(<Button onClick={onClick}>Click me</Button>)

    await userEvent.click(screen.getByText('Click me'))

    expect(onClick).toHaveBeenCalledTimes(1)
  })
})''',
            "api_test": '''// app/api/users/route.test.ts
import { POST } from './route'
import { prismaMock } from '@/tests/mocks/prisma'

describe('POST /api/users', () => {
  it('should create user with valid data', async () => {
    const mockUser = { id: '1', email: 'test@example.com', name: 'Test' }
    prismaMock.user.create.mockResolvedValue(mockUser)

    const request = new Request('http://localhost/api/users', {
      method: 'POST',
      body: JSON.stringify({
        email: 'test@example.com',
        name: 'Test',
        password: 'Password123!',
      }),
    })

    const response = await POST(request)
    const data = await response.json()

    expect(response.status).toBe(201)
    expect(data.data).toEqual(mockUser)
  })
})''',
            "e2e_test": '''// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test('user can sign up and login', async ({ page }) => {
  // Navigate to signup
  await page.goto('/signup')

  // Fill form
  await page.fill('[name="email"]', 'test@example.com')
  await page.fill('[name="password"]', 'Password123!')
  await page.click('button[type="submit"]')

  // Should redirect to dashboard
  await expect(page).toHaveURL('/dashboard')
  await expect(page.locator('h1')).toContainText('Dashboard')
})''',
        }


class DevOpsAgent(Agent):
    """
    Agent specialized in DevOps and deployment.

    Capabilities:
    - CI/CD pipeline setup
    - Deployment strategy
    - Infrastructure as code
    - Monitoring and observability
    """

    name: str = "DevOps Agent"
    role: AgentRole = AgentRole.PRODUCTION
    capabilities: list = [AgentCapability.DEVOPS]

    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute DevOps task.

        Generates:
        - CI/CD pipeline configuration
        - Deployment strategy
        - Infrastructure setup
        - Monitoring plan
        """
        context = self._parse_context(task.description)

        result = {
            "task_id": task.id,
            "task_name": task.name,
            "ci_cd_pipeline": self._design_ci_cd_pipeline(),
            "deployment_strategy": self._plan_deployment_strategy(context),
            "infrastructure": self._design_infrastructure(context),
            "monitoring": self._plan_monitoring(),
            "environments": self._setup_environments(),
            "code_snippets": self._generate_config_files(),
            "confidence": 0.88,
        }

        return result

    def _parse_context(self, description: str) -> Dict[str, Any]:
        """Parse context."""
        return {"platform": "vercel", "scale": "small_to_medium"}

    def _design_ci_cd_pipeline(self) -> Dict[str, Any]:
        """Design CI/CD pipeline."""
        return {
            "platform": "GitHub Actions",
            "workflows": {
                "main": {
                    "trigger": "Push to main",
                    "steps": [
                        "Checkout code",
                        "Setup Node.js 18",
                        "Install dependencies",
                        "Run linting",
                        "Run type checking",
                        "Run tests",
                        "Build application",
                        "Deploy to production (Vercel)",
                    ],
                },
                "pr": {
                    "trigger": "Pull request",
                    "steps": [
                        "Checkout code",
                        "Install dependencies",
                        "Run linting",
                        "Run tests",
                        "Build application",
                        "Deploy preview (Vercel)",
                        "Comment PR with preview URL",
                    ],
                },
            },
            "optimizations": [
                "Cache node_modules between runs",
                "Parallel job execution",
                "Skip deploy on docs-only changes",
                "Use matrix strategy for multi-environment tests",
            ],
        }

    def _plan_deployment_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Plan deployment strategy."""
        platform = context.get("platform", "vercel")

        return {
            "platform": platform,
            "strategy": "Continuous Deployment",
            "environments": {
                "production": {
                    "trigger": "Push to main branch",
                    "url": "app.example.com",
                    "auto_deploy": True,
                },
                "staging": {
                    "trigger": "Push to staging branch",
                    "url": "staging.app.example.com",
                    "auto_deploy": True,
                },
                "preview": {"trigger": "Pull request", "url": "pr-{number}.app.example.com", "auto_deploy": True},
            },
            "rollback": {
                "method": "Vercel instant rollback to previous deployment",
                "trigger": "Manual or automated (error spike)",
            },
            "zero_downtime": {
                "method": "Vercel atomic deploys",
                "health_checks": "Automatic health check before routing traffic",
            },
        }

    def _design_infrastructure(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design infrastructure."""
        return {
            "hosting": {
                "frontend": "Vercel (Next.js optimized)",
                "database": "Supabase or Neon (PostgreSQL)",
                "storage": "Vercel Blob or S3",
                "redis": "Upstash (serverless Redis)",
            },
            "domains": {
                "production": "app.example.com",
                "api": "api.example.com (if separate)",
                "cdn": "Automatic (Vercel Edge Network)",
            },
            "environment_variables": {
                "management": "Vercel dashboard + .env.local (dev)",
                "secrets": ["DATABASE_URL", "NEXTAUTH_SECRET", "STRIPE_SECRET_KEY"],
                "per_environment": True,
            },
            "scaling": {
                "frontend": "Automatic (Vercel serverless)",
                "database": "Vertical scaling (Supabase plans)",
                "strategy": "Start small, scale as needed",
            },
        }

    def _plan_monitoring(self) -> Dict[str, Any]:
        """Plan monitoring and observability."""
        return {
            "application_monitoring": {
                "tool": "Vercel Analytics + Sentry",
                "metrics": [
                    "Request latency (p50, p95, p99)",
                    "Error rates",
                    "Page load times",
                    "API response times",
                ],
            },
            "logging": {
                "platform": "Vercel logs + Datadog/Better Stack",
                "levels": ["error", "warn", "info"],
                "structured": True,
                "retention": "30 days",
            },
            "alerting": {
                "channels": ["Slack", "Email", "PagerDuty"],
                "rules": [
                    "Error rate >1% for 5min → Alert",
                    "API p95 latency >1s for 5min → Alert",
                    "Deployment failure → Alert",
                    "Database connections >80% → Alert",
                ],
            },
            "uptime_monitoring": {"tool": "Better Uptime or Pingdom", "frequency": "1 minute", "locations": "Multiple regions"},
        }

    def _setup_environments(self) -> Dict[str, Dict[str, Any]]:
        """Setup environment configurations."""
        return {
            "development": {
                "database": "Local PostgreSQL or Supabase",
                "env_file": ".env.local",
                "hot_reload": True,
                "debug": True,
            },
            "staging": {
                "database": "Staging Supabase project",
                "url": "staging.app.example.com",
                "data": "Anonymized production data",
                "auto_deploy": True,
            },
            "production": {
                "database": "Production Supabase project",
                "url": "app.example.com",
                "backups": "Automatic daily",
                "monitoring": "Full observability",
            },
        }

    def _generate_config_files(self) -> Dict[str, str]:
        """Generate configuration file examples."""
        return {
            "github_actions": '''# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: 'npm'

      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm run test

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          vercel-args: '--prod'
''',
            "vercel_json": '''{
  "buildCommand": "npm run build",
  "installCommand": "npm ci",
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "Strict-Transport-Security",
          "value": "max-age=31536000; includeSubDomains"
        }
      ]
    }
  ],
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "/api/:path*"
    }
  ]
}''',
        }
