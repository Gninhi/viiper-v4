"""Premium Security & CORS Configuration Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class SecurityConfigSkill(Skill):
    """CORS, security headers, and protection middleware."""

    metadata: SkillMetadata = SkillMetadata(
        name="Security & CORS Configuration",
        slug="security-cors",
        category=SkillCategory.BACKEND_API,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["security", "cors", "helmet", "express", "fastapi", "headers"],
        estimated_time_minutes=20,
        description="Production security with CORS, CSP, and protective headers",
    )

    dependencies: list = [
        Dependency(name="helmet", version="^7.1.0", package_manager="npm", reason="Security headers (Express)"),
        Dependency(name="cors", version="^2.8.5", package_manager="npm", reason="CORS middleware (Express)"),
        Dependency(name="fastapi-cors", version="^0.0.6", package_manager="pip", reason="CORS for FastAPI"),
    ]

    best_practices: list = [
        BestPractice(
            title="Use Helmet for Security Headers",
            description="Helmet sets various HTTP headers for security",
            code_reference="helmet(), CSP, HSTS",
            benefit="Protection against XSS, clickjacking, MIME sniffing",
        ),
        BestPractice(
            title="Whitelist CORS Origins",
            description="Don't use '*' in production",
            code_reference="origin: process.env.ALLOWED_ORIGINS",
            benefit="Prevent unauthorized domains from accessing API",
        ),
        BestPractice(
            title="Enable HTTPS Only",
            description="Use HSTS to force HTTPS",
            code_reference="strictTransportSecurity",
            benefit="Prevent man-in-the-middle attacks",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Express Security Setup",
            description="Apply security middleware",
            code='''import { securityMiddleware, corsConfig } from './middleware/security'

app.use(securityMiddleware)
app.use(corsConfig)''',
        ),
        UsageExample(
            name="FastAPI CORS Setup",
            description="Configure CORS middleware",
            code='''from middleware.security import setup_cors

app = FastAPI()
setup_cors(app)''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="CORS origin: '*' in production",
            why="Any domain can access your API",
            good="Whitelist specific domains",
        ),
        AntiPattern(
            bad="No security headers",
            why="Vulnerable to XSS, clickjacking",
            good="Use helmet or equivalent",
        ),
    ]

    file_structure: dict = {
        "backend/middleware/security.ts": "Security middleware (Express)",
        "backend/middleware/security.py": "Security middleware (FastAPI)",
    }

    express_security: str = '''// backend/middleware/security.ts
import helmet from 'helmet'
import cors from 'cors'
import { Request, Response, NextFunction } from 'express'

// Security headers with Helmet
export const securityMiddleware = helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  hsts: {
    maxAge: 31536000, // 1 year
    includeSubDomains: true,
    preload: true,
  },
  frameguard: {
    action: 'deny', // Prevent clickjacking
  },
  noSniff: true, // Prevent MIME type sniffing
  xssFilter: true,
})

// CORS configuration
const allowedOrigins = process.env.ALLOWED_ORIGINS?.split(',') || [
  'http://localhost:3000',
  'http://localhost:5173',
]

export const corsConfig = cors({
  origin: (origin, callback) => {
    // Allow requests with no origin (mobile apps, Postman, etc.)
    if (!origin) return callback(null, true)

    if (allowedOrigins.includes(origin)) {
      callback(null, true)
    } else {
      callback(new Error('Not allowed by CORS'))
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  exposedHeaders: ['X-Total-Count'],
  maxAge: 86400, // 24 hours
})

// Rate limiting per IP
import rateLimit from 'express-rate-limit'

export const rateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Max 100 requests per window
  message: 'Too many requests from this IP, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
})

// Request sanitization
export function sanitizeInput(req: Request, res: Response, next: NextFunction) {
  // Remove null bytes
  const sanitize = (obj: any): any => {
    if (typeof obj === 'string') {
      return obj.replace(/\0/g, '')
    }
    if (typeof obj === 'object' && obj !== null) {
      Object.keys(obj).forEach(key => {
        obj[key] = sanitize(obj[key])
      })
    }
    return obj
  }

  req.body = sanitize(req.body)
  req.query = sanitize(req.query)
  req.params = sanitize(req.params)
  next()
}
'''

    fastapi_security: str = '''# backend/middleware/security.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import os

def setup_cors(app: FastAPI):
    """Configure CORS middleware."""
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

    if not allowed_origins or allowed_origins == [""]:
        allowed_origins = [
            "http://localhost:3000",
            "http://localhost:5173",
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
        expose_headers=["X-Total-Count"],
        max_age=86400,  # 24 hours
    )

def setup_security_headers(app: FastAPI):
    """Add security headers middleware."""

    class SecurityHeadersMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            response = await call_next(request)

            # Security headers
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
            response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
            response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

            return response

    app.add_middleware(SecurityHeadersMiddleware)

def setup_trusted_hosts(app: FastAPI):
    """Only allow requests from trusted hosts."""
    allowed_hosts = os.getenv("ALLOWED_HOSTS", "").split(",")

    if allowed_hosts and allowed_hosts != [""]:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=allowed_hosts
        )

def setup_rate_limiting(app: FastAPI):
    """Rate limiting middleware (basic implementation)."""
    from collections import defaultdict
    from datetime import datetime, timedelta

    request_counts = defaultdict(list)

    class RateLimitMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            client_ip = request.client.host
            now = datetime.now()

            # Clean old requests (older than 15 minutes)
            request_counts[client_ip] = [
                req_time for req_time in request_counts[client_ip]
                if now - req_time < timedelta(minutes=15)
            ]

            # Check rate limit (100 requests per 15 minutes)
            if len(request_counts[client_ip]) >= 100:
                return Response(
                    content="Too many requests",
                    status_code=429,
                    headers={"Retry-After": "900"}
                )

            request_counts[client_ip].append(now)
            response = await call_next(request)
            return response

    app.add_middleware(RateLimitMiddleware)

def setup_all_security(app: FastAPI):
    """Setup all security middleware."""
    setup_cors(app)
    setup_security_headers(app)
    setup_trusted_hosts(app)
    setup_rate_limiting(app)
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "backend/middleware/security.ts": self.express_security,
            "backend/middleware/security.py": self.fastapi_security,
        }
