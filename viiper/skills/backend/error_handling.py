"""Premium Error Handling Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class ErrorHandlingSkill(Skill):
    """Error handling middleware patterns."""

    metadata: SkillMetadata = SkillMetadata(
        name="Error Handling Middleware",
        slug="error-handling",
        category=SkillCategory.BACKEND_API,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["error", "middleware", "express", "fastapi", "exception"],
        estimated_time_minutes=20,
        description="Production error handling with proper logging and responses",
    )

    dependencies: list = [
        Dependency(name="express", version="^4.18.2", package_manager="npm", reason="Web framework"),
    ]

    best_practices: list = [
        BestPractice(
            title="Never Expose Internal Errors",
            description="Return generic messages in production",
            code_reference="Don't send stack traces to client",
            benefit="Security, no info leakage",
        ),
        BestPractice(
            title="Log All Errors",
            description="Use structured logging",
            code_reference="logger.error({ err, req })",
            benefit="Debugging, monitoring",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Express Error Handler",
            description="Centralized error handling",
            code='''app.use(errorHandler)''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Silent failures",
            why="Errors disappear, impossible to debug",
            good="Always log and return appropriate response",
        ),
    ]

    file_structure: dict = {
        "backend/middleware/errorHandler.ts": "Express error middleware",
        "backend/middleware/exception_handler.py": "FastAPI exception handler",
    }

    express_error_handler: str = '''// backend/middleware/errorHandler.ts
import { Request, Response, NextFunction } from 'express'

export class AppError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public isOperational = true
  ) {
    super(message)
    Object.setPrototypeOf(this, AppError.prototype)
  }
}

export function errorHandler(
  err: Error | AppError,
  req: Request,
  res: Response,
  next: NextFunction
) {
  // Log error
  console.error('[Error]', {
    message: err.message,
    stack: err.stack,
    url: req.url,
    method: req.method
  })

  // Known operational error
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: err.message,
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    })
  }

  // Unknown error - don't leak details
  res.status(500).json({
    error: process.env.NODE_ENV === 'production'
      ? 'Internal server error'
      : err.message
  })
}

// Not found handler
export function notFoundHandler(req: Request, res: Response) {
  res.status(404).json({ error: 'Route not found' })
}
'''

    fastapi_exception_handler: str = '''# backend/middleware/exception_handler.py
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger(__name__)

class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.error(f"AppException: {exc.detail}", extra={"url": str(request.url)})
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": "Validation error", "details": exc.errors()}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Internal server error"}
        )
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "backend/middleware/errorHandler.ts": self.express_error_handler,
            "backend/middleware/exception_handler.py": self.fastapi_exception_handler,
        }
