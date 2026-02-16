"""Premium Rate Limiting Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class RateLimitingSkill(Skill):
    """Advanced rate limiting with Redis and in-memory stores."""

    metadata: SkillMetadata = SkillMetadata(
        name="Rate Limiting",
        slug="rate-limiting",
        category=SkillCategory.BACKEND_API,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["rate-limiting", "throttling", "redis", "security", "ddos"],
        estimated_time_minutes=25,
        description="Protect APIs with per-IP, per-user, and per-endpoint rate limits",
    )

    dependencies: list = [
        Dependency(name="express-rate-limit", version="^7.1.5", package_manager="npm", reason="Rate limiting (Express)"),
        Dependency(name="rate-limit-redis", version="^4.2.0", package_manager="npm", reason="Redis store for rate limits"),
        Dependency(name="slowapi", version="^0.1.9", package_manager="pip", reason="Rate limiting (FastAPI)"),
    ]

    best_practices: list = [
        BestPractice(
            title="Use Different Limits for Different Endpoints",
            description="Auth endpoints stricter than read-only",
            code_reference="login: 5 req/15min, read: 100 req/15min",
            benefit="Prevent brute force, allow normal usage",
        ),
        BestPractice(
            title="Store Rate Limits in Redis",
            description="Share limits across multiple servers",
            code_reference="Redis as shared store",
            benefit="Consistent limits in distributed systems",
        ),
        BestPractice(
            title="Return Retry-After Header",
            description="Tell clients when they can retry",
            code_reference="Retry-After: 900 (seconds)",
            benefit="Better client experience, reduces retries",
        ),
        BestPractice(
            title="Rate Limit by User ID When Authenticated",
            description="Per-user limits more accurate than per-IP",
            code_reference="keyGenerator: (req) => req.user.id",
            benefit="Fair usage, users share IPs (NAT)",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Express Global Rate Limit",
            description="Apply to all routes",
            code='''app.use(rateLimiter({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // 100 requests per window
}))''',
        ),
        UsageExample(
            name="Endpoint-Specific Limit",
            description="Stricter limit for sensitive endpoint",
            code='''app.post('/api/login',
  rateLimiter({ max: 5, windowMs: 15 * 60 * 1000 }),
  loginHandler
)''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Same rate limit for all endpoints",
            why="Auth endpoints need stricter limits",
            good="Different limits per endpoint sensitivity",
        ),
        AntiPattern(
            bad="Only rate limiting by IP",
            why="Shared IPs (NAT, VPNs) affect many users",
            good="Rate limit by user ID when authenticated",
        ),
        AntiPattern(
            bad="No rate limiting",
            why="Easy DoS attacks, API abuse",
            good="Always rate limit public APIs",
        ),
    ]

    file_structure: dict = {
        "backend/middleware/rate-limit.ts": "Rate limiting (Express)",
        "backend/middleware/rate_limit.py": "Rate limiting (FastAPI)",
    }

    rate_limit_ts: str = r'''// backend/middleware/rate-limit.ts
import rateLimit from 'express-rate-limit'
import RedisStore from 'rate-limit-redis'
import { createClient } from 'redis'
import { Request, Response } from 'express'

// Redis client
const redisClient = createClient({
  url: process.env.REDIS_URL || 'redis://localhost:6379',
})

redisClient.connect().catch(console.error)

/**
 * Global rate limiter (apply to all routes)
 */
export const globalRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Max 100 requests per window per IP
  standardHeaders: true, // Return rate limit info in headers
  legacyHeaders: false, // Disable X-RateLimit-* headers
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:global:',
  }),
  message: {
    error: 'Too many requests from this IP, please try again later',
  },
  // Custom handler for when limit is exceeded
  handler: (req: Request, res: Response) => {
    res.status(429).json({
      error: 'Too many requests',
      retryAfter: Math.ceil(req.rateLimit.resetTime! / 1000),
    })
  },
})

/**
 * Strict rate limiter for authentication endpoints
 */
export const authRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // Max 5 login attempts per window
  skipSuccessfulRequests: true, // Don't count successful logins
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:auth:',
  }),
  message: {
    error: 'Too many login attempts, please try again later',
  },
})

/**
 * API rate limiter (higher limits for authenticated users)
 */
export const apiRateLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 60, // 60 requests per minute
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:api:',
  }),
  // Rate limit by user ID if authenticated, otherwise by IP
  keyGenerator: (req: Request) => {
    return req.user?.id || req.ip
  },
})

/**
 * Write operation rate limiter (stricter for mutations)
 */
export const writeRateLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 10, // 10 write operations per minute
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:write:',
  }),
  keyGenerator: (req: Request) => {
    return req.user?.id || req.ip
  },
})

/**
 * Custom rate limiter factory
 */
export function createRateLimiter(options: {
  windowMs: number
  max: number
  prefix: string
  keyGenerator?: (req: Request) => string
}) {
  return rateLimit({
    windowMs: options.windowMs,
    max: options.max,
    store: new RedisStore({
      client: redisClient,
      prefix: `rl:${options.prefix}:`,
    }),
    keyGenerator: options.keyGenerator || ((req: Request) => req.ip),
    standardHeaders: true,
    legacyHeaders: false,
  })
}

// Example usage:
/*
import {
  globalRateLimiter,
  authRateLimiter,
  apiRateLimiter,
  writeRateLimiter
} from './middleware/rate-limit'

// Apply global rate limit to all routes
app.use(globalRateLimiter)

// Stricter limit for auth
app.post('/api/auth/login', authRateLimiter, loginHandler)
app.post('/api/auth/register', authRateLimiter, registerHandler)

// API routes
app.use('/api', apiRateLimiter)

// Write operations
app.post('/api/posts', writeRateLimiter, createPost)
app.put('/api/posts/:id', writeRateLimiter, updatePost)
app.delete('/api/posts/:id', writeRateLimiter, deletePost)
*/
'''

    rate_limit_py: str = r'''# backend/middleware/rate_limit.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request
import redis.asyncio as redis
import os
from typing import Optional

# Redis client for distributed rate limiting
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)

# Key function for per-user rate limiting
def get_user_or_ip(request: Request) -> str:
    """Get user ID if authenticated, otherwise IP address."""
    # Check if user is in request state (set by auth middleware)
    if hasattr(request.state, "user") and request.state.user:
        return f"user:{request.state.user.get('userId')}"
    return get_remote_address(request)

# Create limiter
limiter = Limiter(
    key_func=get_user_or_ip,
    storage_uri=redis_url,
    default_limits=["100 per 15 minutes"],  # Global default
)

# Setup rate limiting for FastAPI
def setup_rate_limiting(app: FastAPI):
    """Add rate limiting to FastAPI app."""
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Rate limit decorators
"""
Example usage:

from fastapi import FastAPI, Request
from backend.middleware.rate_limit import limiter, setup_rate_limiting

app = FastAPI()
setup_rate_limiting(app)

# Global rate limit (100 per 15 minutes) applied automatically

# Stricter limit for auth endpoints
@app.post("/api/auth/login")
@limiter.limit("5 per 15 minutes")
async def login(request: Request):
    pass

# Custom limit for specific endpoint
@app.post("/api/posts")
@limiter.limit("10 per minute")
async def create_post(request: Request):
    pass

# Different limits for different methods
@app.get("/api/posts")
@limiter.limit("60 per minute")
async def get_posts(request: Request):
    pass

# No rate limit for specific endpoint
@app.get("/api/health")
@limiter.exempt
async def health_check():
    return {"status": "ok"}
"""

# Advanced rate limiting with custom Redis
class AdvancedRateLimiter:
    """Advanced rate limiter with custom logic."""

    def __init__(self):
        self.redis = redis_client

    async def check_rate_limit(
        self,
        key: str,
        max_requests: int,
        window_seconds: int
    ) -> tuple[bool, Optional[int]]:
        """
        Check if request exceeds rate limit.

        Returns:
            (is_allowed, retry_after_seconds)
        """
        current_time = int(time.time())
        window_key = f"rl:{key}:{current_time // window_seconds}"

        # Increment counter
        count = await self.redis.incr(window_key)

        # Set expiration on first request in window
        if count == 1:
            await self.redis.expire(window_key, window_seconds)

        # Check if limit exceeded
        if count > max_requests:
            # Calculate retry after
            window_start = (current_time // window_seconds) * window_seconds
            retry_after = (window_start + window_seconds) - current_time
            return False, retry_after

        return True, None

    async def increment(self, key: str, window_seconds: int) -> int:
        """Increment counter and return current count."""
        current_time = int(time.time())
        window_key = f"rl:{key}:{current_time // window_seconds}"

        count = await self.redis.incr(window_key)

        if count == 1:
            await self.redis.expire(window_key, window_seconds)

        return count

    async def reset(self, key: str):
        """Reset rate limit for key."""
        pattern = f"rl:{key}:*"
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)

# Singleton instance
advanced_limiter = AdvancedRateLimiter()

# Dependency for manual rate limiting
import time
from fastapi import HTTPException, status

async def rate_limit_dependency(
    request: Request,
    max_requests: int = 60,
    window_seconds: int = 60
):
    """Dependency for manual rate limiting."""
    # Get user or IP
    if hasattr(request.state, "user") and request.state.user:
        key = f"user:{request.state.user.get('userId')}"
    else:
        key = f"ip:{request.client.host}"

    # Check rate limit
    is_allowed, retry_after = await advanced_limiter.check_rate_limit(
        key, max_requests, window_seconds
    )

    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests",
            headers={"Retry-After": str(retry_after)}
        )
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "backend/middleware/rate-limit.ts": self.rate_limit_ts,
            "backend/middleware/rate_limit.py": self.rate_limit_py,
        }
