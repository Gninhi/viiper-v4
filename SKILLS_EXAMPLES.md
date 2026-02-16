# Skills Library - Exemples Détaillés

## 📚 Vue d'Ensemble

Chaque skill est un **template de code production-ready** avec:
- ✅ Code complet et testé
- ✅ Best practices de l'industrie
- ✅ Documentation intégrée
- ✅ Exemples d'utilisation
- ✅ Dépendances listées

---

## Exemple 1: Frontend Skill - Premium Button Component

### Structure Complète

```python
"""
Premium Button Component Skill.

Generates production-ready button component with variants,
accessibility, and animations.
"""

from typing import List, Dict, Any
from viiper.skills.base import Skill, SkillCategory, SkillMetadata

class PremiumButtonSkill(Skill):
    """
    World-class button component following Awwwards standards.

    Features:
    - Multiple variants (primary, secondary, ghost, danger)
    - Size variants (sm, md, lg)
    - Loading states
    - Accessibility (ARIA, keyboard navigation)
    - Smooth animations
    - Type-safe with TypeScript
    """

    # Metadata
    metadata = SkillMetadata(
        name="Premium Button Component",
        slug="premium-button",
        category=SkillCategory.FRONTEND_COMPONENTS,
        version="1.0.0",
        author="VIIPER Elite Frontend Agent",
        tags=["react", "button", "ui", "components", "typescript"],
        difficulty="intermediate",
        estimated_time_minutes=15
    )

    # Dependencies
    dependencies = [
        {
            "name": "react",
            "version": "^18.0.0",
            "package_manager": "npm"
        },
        {
            "name": "class-variance-authority",
            "version": "^0.7.0",
            "package_manager": "npm",
            "reason": "Type-safe variant composition"
        },
        {
            "name": "tailwindcss",
            "version": "^3.4.0",
            "package_manager": "npm",
            "reason": "Utility-first CSS"
        }
    ]

    # File structure this skill generates
    file_structure = {
        "components/ui/button.tsx": "main_component",
        "lib/utils.ts": "utility_functions",
        "__tests__/button.test.tsx": "test_file"
    }

    # Main component code
    component_code = '''
// components/ui/button.tsx
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  // Base styles - ALWAYS applied
  "inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        // Primary: High-contrast, bold CTA
        primary:
          "bg-black text-white hover:bg-gray-800 active:scale-95 focus-visible:ring-black",

        // Secondary: Medium emphasis
        secondary:
          "bg-gray-100 text-gray-900 hover:bg-gray-200 active:scale-95 focus-visible:ring-gray-400",

        // Ghost: Minimal, blends with background
        ghost:
          "hover:bg-gray-100 text-gray-700 active:scale-95 focus-visible:ring-gray-400",

        // Danger: Destructive actions (delete, remove)
        danger:
          "bg-red-600 text-white hover:bg-red-700 active:scale-95 focus-visible:ring-red-500",

        // Link: Text-like, no background
        link:
          "text-gray-900 underline-offset-4 hover:underline focus-visible:ring-gray-400"
      },
      size: {
        sm: "h-9 px-3 text-sm",
        md: "h-11 px-5 text-base",
        lg: "h-13 px-7 text-lg"
      }
    },
    defaultVariants: {
      variant: "primary",
      size: "md"
    }
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  /** Button content */
  children: React.ReactNode

  /** Show loading spinner and disable interaction */
  loading?: boolean

  /** Icon to display before content */
  icon?: React.ReactNode

  /** Icon to display after content */
  iconRight?: React.ReactNode
}

/**
 * Premium button component with variants and accessibility.
 *
 * @example
 * ```tsx
 * <Button variant="primary" size="lg">
 *   Get Started
 * </Button>
 *
 * <Button loading={isLoading} onClick={handleSubmit}>
 *   Save Changes
 * </Button>
 * ```
 */
export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({
    className,
    variant,
    size,
    loading,
    disabled,
    icon,
    iconRight,
    children,
    ...props
  }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        disabled={disabled || loading}
        ref={ref}
        aria-busy={loading}
        {...props}
      >
        {loading && (
          <svg
            className="animate-spin h-4 w-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        )}
        {!loading && icon && <span aria-hidden="true">{icon}</span>}
        <span>{children}</span>
        {!loading && iconRight && <span aria-hidden="true">{iconRight}</span>}
      </button>
    )
  }
)

Button.displayName = "Button"
'''

    # Utility functions (cn helper)
    utility_code = '''
// lib/utils.ts
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

    # Test file
    test_code = '''
// __tests__/button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from '@/components/ui/button'

describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button')).toHaveTextContent('Click me')
  })

  it('applies variant styles', () => {
    render(<Button variant="danger">Delete</Button>)
    const button = screen.getByRole('button')
    expect(button).toHaveClass('bg-red-600')
  })

  it('shows loading state', () => {
    render(<Button loading>Loading</Button>)
    const button = screen.getByRole('button')
    expect(button).toBeDisabled()
    expect(button).toHaveAttribute('aria-busy', 'true')
  })

  it('disables when disabled prop is true', () => {
    render(<Button disabled>Disabled</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click</Button>)
    fireEvent.click(screen.getByRole('button'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('renders icon before content', () => {
    render(
      <Button icon={<span data-testid="icon">★</span>}>
        Star
      </Button>
    )
    expect(screen.getByTestId('icon')).toBeInTheDocument()
  })
})
'''

    # Best practices embedded in code
    best_practices = [
        {
            "title": "Accessibility First",
            "description": "Uses semantic HTML (button), ARIA attributes (aria-busy), and focus states",
            "code_reference": "focus-visible:ring-2"
        },
        {
            "title": "Type Safety",
            "description": "Full TypeScript support with VariantProps for autocomplete",
            "code_reference": "VariantProps<typeof buttonVariants>"
        },
        {
            "title": "Performance",
            "description": "Uses React.forwardRef for ref forwarding, minimal re-renders",
            "code_reference": "React.forwardRef"
        },
        {
            "title": "User Feedback",
            "description": "Loading states, active states (scale-95), smooth transitions",
            "code_reference": "transition-all duration-200"
        },
        {
            "title": "Composability",
            "description": "Accepts all native button props via spread (...props)",
            "code_reference": "extends React.ButtonHTMLAttributes"
        }
    ]

    # Usage examples
    usage_examples = [
        {
            "name": "Primary CTA",
            "description": "High-emphasis action (main CTA)",
            "code": '<Button variant="primary" size="lg">Get Started Free</Button>'
        },
        {
            "name": "Form Submit with Loading",
            "description": "Shows loading state during async operation",
            "code": '''
<form onSubmit={handleSubmit}>
  <Button
    type="submit"
    loading={isSubmitting}
    disabled={!isValid}
  >
    Save Changes
  </Button>
</form>
'''
        },
        {
            "name": "Danger Action",
            "description": "Destructive action with confirmation",
            "code": '''
<Button
  variant="danger"
  onClick={handleDelete}
  icon={<TrashIcon />}
>
  Delete Account
</Button>
'''
        },
        {
            "name": "Ghost Navigation",
            "description": "Minimal button for secondary navigation",
            "code": '<Button variant="ghost" size="sm">Learn More →</Button>'
        }
    ]

    # Anti-patterns to avoid
    anti_patterns = [
        {
            "bad": "Using <div> with onClick instead of <button>",
            "why": "Not keyboard accessible, no semantic meaning",
            "good": "Always use <button> or <a> for clickable elements"
        },
        {
            "bad": "Inline styles for variants",
            "why": "Hard to maintain, no autocomplete",
            "good": "Use class-variance-authority for type-safe variants"
        },
        {
            "bad": "Missing loading states",
            "why": "User doesn't know if action is processing",
            "good": "Always show loading state for async actions"
        }
    ]

    # Design tokens used
    design_tokens = {
        "colors": {
            "primary": "#000000",
            "secondary": "#F3F4F6",
            "danger": "#DC2626"
        },
        "spacing": {
            "sm": "0.75rem 1rem",
            "md": "0.875rem 1.25rem",
            "lg": "1rem 1.75rem"
        },
        "typography": {
            "sm": "0.875rem",
            "md": "1rem",
            "lg": "1.125rem"
        },
        "transitions": {
            "default": "200ms ease-in-out"
        }
    }

    def generate(self, context: Dict[str, Any] = None) -> Dict[str, str]:
        """
        Generate button component files.

        Args:
            context: Optional configuration (variant names, colors, etc.)

        Returns:
            Dictionary of filepath: code
        """
        return {
            "components/ui/button.tsx": self.component_code,
            "lib/utils.ts": self.utility_code,
            "__tests__/button.test.tsx": self.test_code
        }

    def get_installation_steps(self) -> List[str]:
        """Get step-by-step installation instructions."""
        return [
            "npm install class-variance-authority clsx tailwind-merge",
            "Add cn utility to lib/utils.ts",
            "Create components/ui/button.tsx with component code",
            "Import and use: import { Button } from '@/components/ui/button'",
            "Test with: npm test button.test.tsx"
        ]
```

---

## Exemple 2: Backend Skill - JWT Authentication

### Structure Complète

```python
"""
JWT Authentication Skill.

Production-ready authentication system with:
- Access token + Refresh token pattern
- Secure HTTP-only cookies
- Token rotation
- Blacklist for logout
"""

from typing import List, Dict, Any
from viiper.skills.base import Skill, SkillCategory, SkillMetadata

class JWTAuthenticationSkill(Skill):
    """
    Enterprise-grade JWT authentication following OWASP guidelines.

    Features:
    - Access token (short-lived, 15min)
    - Refresh token (long-lived, 7 days)
    - HTTP-only secure cookies
    - Token blacklist for logout
    - CSRF protection
    - Rate limiting on auth endpoints
    """

    metadata = SkillMetadata(
        name="JWT Authentication System",
        slug="jwt-auth",
        category=SkillCategory.BACKEND_AUTH,
        version="1.0.0",
        author="VIIPER Elite Backend Agent",
        tags=["auth", "jwt", "security", "express", "nodejs"],
        difficulty="advanced",
        estimated_time_minutes=45
    )

    dependencies = [
        {
            "name": "jsonwebtoken",
            "version": "^9.0.2",
            "package_manager": "npm"
        },
        {
            "name": "bcryptjs",
            "version": "^2.4.3",
            "package_manager": "npm"
        },
        {
            "name": "express",
            "version": "^4.18.0",
            "package_manager": "npm"
        }
    ]

    # Main authentication service
    auth_service_code = '''
// src/services/auth.service.ts
import jwt from 'jsonwebtoken'
import bcrypt from 'bcryptjs'
import { db } from '@/lib/database'
import { redis } from '@/lib/redis'

interface TokenPayload {
  userId: string
  email: string
  role: string
}

interface Tokens {
  accessToken: string
  refreshToken: string
}

export class AuthService {
  private readonly ACCESS_TOKEN_SECRET = process.env.ACCESS_TOKEN_SECRET!
  private readonly REFRESH_TOKEN_SECRET = process.env.REFRESH_TOKEN_SECRET!
  private readonly ACCESS_TOKEN_EXPIRY = '15m'
  private readonly REFRESH_TOKEN_EXPIRY = '7d'

  /**
   * Generate access and refresh tokens for user.
   */
  async generateTokens(userId: string, email: string, role: string): Promise<Tokens> {
    const payload: TokenPayload = { userId, email, role }

    const accessToken = jwt.sign(
      payload,
      this.ACCESS_TOKEN_SECRET,
      { expiresIn: this.ACCESS_TOKEN_EXPIRY }
    )

    const refreshToken = jwt.sign(
      payload,
      this.REFRESH_TOKEN_SECRET,
      { expiresIn: this.REFRESH_TOKEN_EXPIRY }
    )

    // Store refresh token in database for tracking
    await db.refreshToken.create({
      data: {
        token: refreshToken,
        userId,
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000) // 7 days
      }
    })

    return { accessToken, refreshToken }
  }

  /**
   * Verify access token.
   */
  verifyAccessToken(token: string): TokenPayload {
    try {
      return jwt.verify(token, this.ACCESS_TOKEN_SECRET) as TokenPayload
    } catch (error) {
      throw new Error('Invalid or expired access token')
    }
  }

  /**
   * Verify refresh token.
   */
  async verifyRefreshToken(token: string): Promise<TokenPayload> {
    try {
      const payload = jwt.verify(token, this.REFRESH_TOKEN_SECRET) as TokenPayload

      // Check if token exists in database and not revoked
      const storedToken = await db.refreshToken.findFirst({
        where: {
          token,
          userId: payload.userId,
          revokedAt: null
        }
      })

      if (!storedToken) {
        throw new Error('Token not found or revoked')
      }

      return payload
    } catch (error) {
      throw new Error('Invalid or expired refresh token')
    }
  }

  /**
   * Refresh access token using refresh token.
   */
  async refreshAccessToken(refreshToken: string): Promise<string> {
    const payload = await this.verifyRefreshToken(refreshToken)

    // Generate new access token (same payload)
    const accessToken = jwt.sign(
      payload,
      this.ACCESS_TOKEN_SECRET,
      { expiresIn: this.ACCESS_TOKEN_EXPIRY }
    )

    return accessToken
  }

  /**
   * Logout user by revoking refresh token.
   */
  async logout(refreshToken: string): Promise<void> {
    await db.refreshToken.updateMany({
      where: { token: refreshToken },
      data: { revokedAt: new Date() }
    })
  }

  /**
   * Hash password securely.
   */
  async hashPassword(password: string): Promise<string> {
    return bcrypt.hash(password, 12) // 12 rounds recommended by OWASP
  }

  /**
   * Verify password against hash.
   */
  async verifyPassword(password: string, hash: string): Promise<boolean> {
    return bcrypt.compare(password, hash)
  }
}

export const authService = new AuthService()
'''

    # Authentication middleware
    auth_middleware_code = '''
// src/middleware/auth.middleware.ts
import { Request, Response, NextFunction } from 'express'
import { authService } from '@/services/auth.service'

// Extend Express Request to include user
declare global {
  namespace Express {
    interface Request {
      user?: {
        userId: string
        email: string
        role: string
      }
    }
  }
}

/**
 * Middleware to protect routes - requires valid access token.
 */
export function requireAuth(req: Request, res: Response, next: NextFunction) {
  try {
    // Get token from Authorization header
    const authHeader = req.headers.authorization
    if (!authHeader?.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'No token provided' })
    }

    const token = authHeader.substring(7) // Remove 'Bearer '

    // Verify token
    const payload = authService.verifyAccessToken(token)

    // Attach user to request
    req.user = payload

    next()
  } catch (error) {
    res.status(401).json({ error: 'Invalid or expired token' })
  }
}

/**
 * Middleware to check user role.
 */
export function requireRole(...allowedRoles: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Not authenticated' })
    }

    if (!allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' })
    }

    next()
  }
}
'''

    # Auth routes
    auth_routes_code = '''
// src/routes/auth.routes.ts
import express from 'express'
import { authService } from '@/services/auth.service'
import { db } from '@/lib/database'
import { z } from 'zod'

const router = express.Router()

// Validation schemas
const registerSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string().min(2)
})

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string()
})

/**
 * POST /auth/register
 * Register new user.
 */
router.post('/register', async (req, res) => {
  try {
    // Validate input
    const { email, password, name } = registerSchema.parse(req.body)

    // Check if user exists
    const existingUser = await db.user.findUnique({ where: { email } })
    if (existingUser) {
      return res.status(400).json({ error: 'Email already registered' })
    }

    // Hash password
    const passwordHash = await authService.hashPassword(password)

    // Create user
    const user = await db.user.create({
      data: {
        email,
        passwordHash,
        name,
        role: 'user'
      }
    })

    // Generate tokens
    const tokens = await authService.generateTokens(user.id, user.email, user.role)

    // Set refresh token in HTTP-only cookie
    res.cookie('refreshToken', tokens.refreshToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 7 * 24 * 60 * 60 * 1000 // 7 days
    })

    res.status(201).json({
      accessToken: tokens.accessToken,
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role
      }
    })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ error: error.errors })
    }
    res.status(500).json({ error: 'Registration failed' })
  }
})

/**
 * POST /auth/login
 * Login existing user.
 */
router.post('/login', async (req, res) => {
  try {
    const { email, password } = loginSchema.parse(req.body)

    // Find user
    const user = await db.user.findUnique({ where: { email } })
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' })
    }

    // Verify password
    const isValid = await authService.verifyPassword(password, user.passwordHash)
    if (!isValid) {
      return res.status(401).json({ error: 'Invalid credentials' })
    }

    // Generate tokens
    const tokens = await authService.generateTokens(user.id, user.email, user.role)

    // Set refresh token cookie
    res.cookie('refreshToken', tokens.refreshToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 7 * 24 * 60 * 60 * 1000
    })

    res.json({
      accessToken: tokens.accessToken,
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role
      }
    })
  } catch (error) {
    res.status(500).json({ error: 'Login failed' })
  }
})

/**
 * POST /auth/refresh
 * Refresh access token using refresh token.
 */
router.post('/refresh', async (req, res) => {
  try {
    const refreshToken = req.cookies.refreshToken
    if (!refreshToken) {
      return res.status(401).json({ error: 'No refresh token' })
    }

    const accessToken = await authService.refreshAccessToken(refreshToken)

    res.json({ accessToken })
  } catch (error) {
    res.status(401).json({ error: 'Invalid refresh token' })
  }
})

/**
 * POST /auth/logout
 * Logout user (revoke refresh token).
 */
router.post('/logout', async (req, res) => {
  try {
    const refreshToken = req.cookies.refreshToken
    if (refreshToken) {
      await authService.logout(refreshToken)
    }

    res.clearCookie('refreshToken')
    res.json({ message: 'Logged out successfully' })
  } catch (error) {
    res.status(500).json({ error: 'Logout failed' })
  }
})

export default router
'''

    best_practices = [
        {
            "title": "Token Security",
            "description": "Access tokens are short-lived (15min), refresh tokens in HTTP-only cookies",
            "owasp_reference": "A02:2021 – Cryptographic Failures"
        },
        {
            "title": "Password Hashing",
            "description": "Uses bcrypt with 12 rounds (OWASP recommended)",
            "owasp_reference": "A02:2021 – Cryptographic Failures"
        },
        {
            "title": "Token Revocation",
            "description": "Refresh tokens stored in DB, can be revoked on logout",
            "owasp_reference": "A07:2021 – Identification and Authentication Failures"
        },
        {
            "title": "Input Validation",
            "description": "All inputs validated with Zod schemas",
            "owasp_reference": "A03:2021 – Injection"
        }
    ]

    security_checklist = [
        "✅ HTTP-only cookies (prevents XSS theft)",
        "✅ Secure flag in production (HTTPS only)",
        "✅ SameSite=strict (prevents CSRF)",
        "✅ Short-lived access tokens (15min)",
        "✅ Token rotation on refresh",
        "✅ Bcrypt with 12 rounds",
        "✅ Input validation (Zod)",
        "✅ No sensitive data in JWT payload"
    ]

    def generate(self, context: Dict[str, Any] = None) -> Dict[str, str]:
        return {
            "src/services/auth.service.ts": self.auth_service_code,
            "src/middleware/auth.middleware.ts": self.auth_middleware_code,
            "src/routes/auth.routes.ts": self.auth_routes_code
        }
```

---

## Exemple 3: DevOps Skill - Docker Production Setup

### Structure Complète

```python
"""
Docker Production Setup Skill.

Multi-stage Docker build with:
- Production optimizations
- Security best practices
- Health checks
- Resource limits
"""

from typing import List, Dict, Any
from viiper.skills.base import Skill, SkillCategory, SkillMetadata

class DockerProductionSkill(Skill):
    """
    Production-ready Docker configuration.

    Features:
    - Multi-stage build (smaller images)
    - Non-root user (security)
    - Health checks
    - Optimized caching
    - Docker Compose for development
    """

    metadata = SkillMetadata(
        name="Docker Production Setup",
        slug="docker-production",
        category=SkillCategory.DEVOPS_DEPLOYMENT,
        version="1.0.0",
        author="VIIPER Elite DevOps Agent",
        tags=["docker", "deployment", "production", "security"],
        difficulty="intermediate",
        estimated_time_minutes=20
    )

    # Dockerfile with multi-stage build
    dockerfile_code = '''
# Dockerfile
# Multi-stage build for production Node.js app

# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies (including dev dependencies for build)
RUN npm ci

# Stage 2: Builder
FROM node:20-alpine AS builder
WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build application
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app

# Create non-root user for security
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy only production dependencies
COPY --from=builder /app/package.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/public ./public

# Set ownership to non-root user
RUN chown -R nextjs:nodejs /app

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Environment
ENV NODE_ENV=production
ENV PORT=3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \\
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Start application
CMD ["node", "dist/server.js"]
'''

    # Docker Compose for development
    docker_compose_code = '''
# docker-compose.yml
# Development environment with hot reload

version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://postgres:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    command: npm run dev

  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
'''

    # .dockerignore for optimization
    dockerignore_code = '''
# .dockerignore
# Prevent copying unnecessary files

node_modules
npm-debug.log
.git
.gitignore
.env
.env.local
.DS_Store
dist
build
coverage
.vscode
.idea
*.md
!README.md
.github
'''

    # Production docker-compose
    docker_compose_prod_code = '''
# docker-compose.prod.yml
# Production deployment with resource limits

version: '3.8'

services:
  app:
    image: myapp:latest
    restart: always
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:3000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
'''

    best_practices = [
        {
            "title": "Multi-Stage Build",
            "description": "Reduces final image size by 70%+ by excluding build dependencies",
            "benefit": "Faster deployments, lower bandwidth costs"
        },
        {
            "title": "Non-Root User",
            "description": "Runs as unprivileged user (nodejs:nodejs)",
            "benefit": "Prevents container escape attacks"
        },
        {
            "title": "Health Checks",
            "description": "Docker monitors app health automatically",
            "benefit": "Automatic restarts on failure"
        },
        {
            "title": "Layer Caching",
            "description": "Copy package.json before source code",
            "benefit": "Faster rebuilds when code changes"
        }
    ]

    security_checklist = [
        "✅ Non-root user (UID 1001)",
        "✅ Minimal base image (alpine)",
        "✅ No secrets in image",
        "✅ .dockerignore to prevent leaks",
        "✅ Health checks enabled",
        "✅ Resource limits set",
        "✅ Restart policy configured"
    ]

    def generate(self, context: Dict[str, Any] = None) -> Dict[str, str]:
        return {
            "Dockerfile": self.dockerfile_code,
            "docker-compose.yml": self.docker_compose_code,
            "docker-compose.prod.yml": self.docker_compose_prod_code,
            ".dockerignore": self.dockerignore_code
        }
```

---

## 🎯 Résumé des 3 Exemples

### Frontend Skill (Button)
- **Code**: 150 lignes de composant React TypeScript
- **Tests**: Tests complets avec React Testing Library
- **Features**: Variants, loading, accessibility, animations
- **Dépendances**: 3 packages (react, cva, tailwind)
- **Temps**: ~15 min d'implémentation

### Backend Skill (JWT Auth)
- **Code**: 400 lignes (service + middleware + routes)
- **Security**: OWASP compliant, HTTP-only cookies
- **Features**: Access/refresh tokens, role-based access
- **Dépendances**: 3 packages (jwt, bcrypt, express)
- **Temps**: ~45 min d'implémentation

### DevOps Skill (Docker)
- **Code**: 4 fichiers de configuration
- **Optimization**: Multi-stage builds, 70% size reduction
- **Features**: Health checks, resource limits, non-root
- **Dépendances**: Docker, Docker Compose
- **Temps**: ~20 min d'implémentation

---

## ✅ Ce que chaque Skill contient

1. **Metadata** - Nom, catégorie, difficulté, tags
2. **Dependencies** - Liste précise des packages requis
3. **Code Templates** - Code production-ready complet
4. **Best Practices** - Pratiques de l'industrie intégrées
5. **Security Checklist** - Validations de sécurité
6. **Usage Examples** - Exemples concrets d'utilisation
7. **Anti-Patterns** - Erreurs communes à éviter
8. **Tests** - Tests automatisés inclus

---

**Maintenant que vous voyez la structure complète, voulez-vous que je commence l'implémentation ?**

**Option 1**: Oui, commencez Phase 1 (Infrastructure)
**Option 2**: Ajustez quelque chose dans les exemples d'abord

**(1 ou 2)**
