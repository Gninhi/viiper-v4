"""Premium Health Checks & Monitoring Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class HealthChecksSkill(Skill):
    """Health check endpoints for monitoring and orchestration."""

    metadata: SkillMetadata = SkillMetadata(
        name="Health Checks & Monitoring",
        slug="health-checks",
        category=SkillCategory.BACKEND_API,
        difficulty=SkillDifficulty.BEGINNER,
        tags=["health", "monitoring", "kubernetes", "docker", "observability"],
        estimated_time_minutes=15,
        description="Health check endpoints for liveness, readiness, and dependency monitoring",
    )

    dependencies: list = []

    best_practices: list = [
        BestPractice(
            title="Implement Liveness and Readiness Probes",
            description="Liveness: is app running? Readiness: can app serve traffic?",
            code_reference="/health/live and /health/ready",
            benefit="Kubernetes/Docker can restart unhealthy containers",
        ),
        BestPractice(
            title="Check Critical Dependencies",
            description="Test DB, Redis, external APIs",
            code_reference="Check DB connection, ping Redis",
            benefit="Detect issues before they affect users",
        ),
        BestPractice(
            title="Return Detailed Status in Dev",
            description="Show which checks failed",
            code_reference="{ db: 'ok', redis: 'error' }",
            benefit="Faster debugging",
        ),
        BestPractice(
            title="Keep Health Checks Fast",
            description="Timeout in < 1 second",
            code_reference="Fast connection pings, not heavy queries",
            benefit="Don't slow down orchestration",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Kubernetes Liveness Probe",
            description="Check if app is alive",
            code='''livenessProbe:
  httpGet:
    path: /health/live
    port: 3000
  initialDelaySeconds: 30
  periodSeconds: 10''',
        ),
        UsageExample(
            name="Readiness Probe",
            description="Check if app is ready",
            code='''readinessProbe:
  httpGet:
    path: /health/ready
    port: 3000
  periodSeconds: 5''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="No health check endpoint",
            why="Orchestrators can't detect failures",
            good="Implement /health endpoints",
        ),
        AntiPattern(
            bad="Health check does heavy work",
            why="Slows down Kubernetes, times out",
            good="Fast checks (< 1 second)",
        ),
        AntiPattern(
            bad="Always return 200 OK",
            why="Doesn't detect actual issues",
            good="Check dependencies, return errors",
        ),
    ]

    file_structure: dict = {
        "backend/routes/health.ts": "Health check routes (Express)",
        "backend/routers/health.py": "Health check routes (FastAPI)",
    }

    health_routes_ts: str = r'''// backend/routes/health.ts
import { Router, Request, Response } from 'express'
import { PrismaClient } from '@prisma/client'
import { createClient } from 'redis'

const router = Router()
const prisma = new PrismaClient()

const redisClient = createClient({
  url: process.env.REDIS_URL || 'redis://localhost:6379',
})

redisClient.connect().catch(console.error)

/**
 * Liveness probe - is the app alive?
 * Simple check that the process is running
 */
router.get('/live', (req: Request, res: Response) => {
  res.status(200).json({
    status: 'ok',
    timestamp: new Date().toISOString(),
  })
})

/**
 * Readiness probe - is the app ready to serve traffic?
 * Checks critical dependencies
 */
router.get('/ready', async (req: Request, res: Response) => {
  const checks: Record<string, { status: string; message?: string; duration?: number }> = {}

  // Check database
  try {
    const start = Date.now()
    await prisma.$queryRaw`SELECT 1`
    checks.database = {
      status: 'ok',
      duration: Date.now() - start,
    }
  } catch (error: any) {
    checks.database = {
      status: 'error',
      message: error.message,
    }
  }

  // Check Redis
  try {
    const start = Date.now()
    await redisClient.ping()
    checks.redis = {
      status: 'ok',
      duration: Date.now() - start,
    }
  } catch (error: any) {
    checks.redis = {
      status: 'error',
      message: error.message,
    }
  }

  // Determine overall status
  const hasErrors = Object.values(checks).some(check => check.status === 'error')
  const overallStatus = hasErrors ? 'error' : 'ok'

  const statusCode = overallStatus === 'ok' ? 200 : 503

  res.status(statusCode).json({
    status: overallStatus,
    timestamp: new Date().toISOString(),
    checks: process.env.NODE_ENV === 'development' ? checks : undefined,
  })
})

/**
 * Detailed health check
 * Returns comprehensive system status
 */
router.get('/', async (req: Request, res: Response) => {
  const checks: Record<string, any> = {}

  // Database check
  try {
    const start = Date.now()
    await prisma.$queryRaw`SELECT 1`
    const duration = Date.now() - start
    checks.database = {
      status: 'ok',
      responseTime: `${duration}ms`,
    }
  } catch (error: any) {
    checks.database = {
      status: 'error',
      error: error.message,
    }
  }

  // Redis check
  try {
    const start = Date.now()
    await redisClient.ping()
    const duration = Date.now() - start
    checks.redis = {
      status: 'ok',
      responseTime: `${duration}ms`,
    }
  } catch (error: any) {
    checks.redis = {
      status: 'error',
      error: error.message,
    }
  }

  // System info
  const systemInfo = {
    uptime: process.uptime(),
    memory: {
      total: Math.round(process.memoryUsage().heapTotal / 1024 / 1024) + ' MB',
      used: Math.round(process.memoryUsage().heapUsed / 1024 / 1024) + ' MB',
    },
    nodeVersion: process.version,
    environment: process.env.NODE_ENV,
  }

  const hasErrors = Object.values(checks).some((check: any) => check.status === 'error')
  const statusCode = hasErrors ? 503 : 200

  res.status(statusCode).json({
    status: hasErrors ? 'error' : 'healthy',
    timestamp: new Date().toISOString(),
    system: systemInfo,
    checks,
  })
})

export default router

// Example usage in app.ts:
/*
import healthRoutes from './routes/health'

app.use('/health', healthRoutes)
*/
'''

    health_routers_py: str = r'''# backend/routers/health.py
from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
import time
import psutil
import os

router = APIRouter(prefix="/health", tags=["health"])

class HealthStatus(BaseModel):
    """Health status response."""
    status: str
    timestamp: str
    checks: Optional[Dict[str, Any]] = None
    system: Optional[Dict[str, Any]] = None

@router.get("/live", status_code=status.HTTP_200_OK)
async def liveness():
    """
    Liveness probe - is the app alive?

    Used by Kubernetes to determine if container should be restarted.
    Should be simple and fast.
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness():
    """
    Readiness probe - is the app ready to serve traffic?

    Used by Kubernetes to determine if pod should receive traffic.
    Checks critical dependencies.
    """
    checks = {}

    # Check database
    try:
        from backend.database import engine
        start = time.time()

        async with engine.begin() as conn:
            await conn.execute("SELECT 1")

        duration = (time.time() - start) * 1000  # ms
        checks["database"] = {
            "status": "ok",
            "duration": f"{duration:.2f}ms"
        }
    except Exception as e:
        checks["database"] = {
            "status": "error",
            "message": str(e)
        }

    # Check Redis
    try:
        from backend.lib.cache import cache
        start = time.time()

        await cache.client.ping()

        duration = (time.time() - start) * 1000  # ms
        checks["redis"] = {
            "status": "ok",
            "duration": f"{duration:.2f}ms"
        }
    except Exception as e:
        checks["redis"] = {
            "status": "error",
            "message": str(e)
        }

    # Determine overall status
    has_errors = any(check["status"] == "error" for check in checks.values())
    overall_status = "error" if has_errors else "ok"

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE if has_errors else status.HTTP_200_OK

    response = {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
    }

    # Include check details in development
    if os.getenv("ENVIRONMENT") == "development":
        response["checks"] = checks

    return response

@router.get("/", response_model=HealthStatus)
async def health_check():
    """
    Detailed health check with system info.

    Returns comprehensive status of application and dependencies.
    """
    checks = {}

    # Database check
    try:
        from backend.database import engine
        start = time.time()

        async with engine.begin() as conn:
            await conn.execute("SELECT 1")

        duration = (time.time() - start) * 1000
        checks["database"] = {
            "status": "ok",
            "responseTime": f"{duration:.2f}ms"
        }
    except Exception as e:
        checks["database"] = {
            "status": "error",
            "error": str(e)
        }

    # Redis check
    try:
        from backend.lib.cache import cache
        start = time.time()

        await cache.client.ping()

        duration = (time.time() - start) * 1000
        checks["redis"] = {
            "status": "ok",
            "responseTime": f"{duration:.2f}ms"
        }
    except Exception as e:
        checks["redis"] = {
            "status": "error",
            "error": str(e)
        }

    # System info
    process = psutil.Process(os.getpid())
    system_info = {
        "uptime": time.time() - process.create_time(),
        "memory": {
            "total": f"{process.memory_info().rss / 1024 / 1024:.2f} MB",
            "percent": f"{process.memory_percent():.2f}%"
        },
        "cpu_percent": f"{process.cpu_percent()}%",
        "python_version": os.sys.version.split()[0],
        "environment": os.getenv("ENVIRONMENT", "unknown")
    }

    # Determine status
    has_errors = any(check["status"] == "error" for check in checks.values())

    return {
        "status": "error" if has_errors else "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "system": system_info,
        "checks": checks
    }

# Example usage in main.py:
"""
from backend.routers.health import router as health_router

app = FastAPI()
app.include_router(health_router)
"""
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "backend/routes/health.ts": self.health_routes_ts,
            "backend/routers/health.py": self.health_routers_py,
        }
