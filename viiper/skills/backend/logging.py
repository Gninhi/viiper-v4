"""Premium Logging Patterns Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class LoggingSkill(Skill):
    """Structured logging with Winston and Python logging."""

    metadata: SkillMetadata = SkillMetadata(
        name="Structured Logging",
        slug="logging",
        category=SkillCategory.BACKEND_API,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["logging", "winston", "observability", "debugging", "monitoring"],
        estimated_time_minutes=20,
        description="Production logging with structured data, log levels, and rotation",
    )

    dependencies: list = [
        Dependency(name="winston", version="^3.11.0", package_manager="npm", reason="Logging library (Node.js)"),
        Dependency(name="winston-daily-rotate-file", version="^4.7.1", package_manager="npm", reason="Log rotation"),
        Dependency(name="python-json-logger", version="^2.0.7", package_manager="pip", reason="JSON logging (Python)"),
    ]

    best_practices: list = [
        BestPractice(
            title="Use Structured Logging",
            description="Log objects, not strings",
            code_reference='logger.info({ userId, action: "login" })',
            benefit="Searchable, filterable in log aggregators",
        ),
        BestPractice(
            title="Log Levels Appropriately",
            description="ERROR for failures, INFO for events, DEBUG for details",
            code_reference="logger.error, logger.info, logger.debug",
            benefit="Filter logs by severity",
        ),
        BestPractice(
            title="Include Context",
            description="Add request ID, user ID, trace ID",
            code_reference="{ requestId, userId, ...data }",
            benefit="Trace requests through system",
        ),
        BestPractice(
            title="Rotate Log Files",
            description="Daily rotation, max size limits",
            code_reference="maxSize: '20m', maxFiles: '14d'",
            benefit="Prevent disk space issues",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Structured Log",
            description="Log with context",
            code='''logger.info({
  message: 'User logged in',
  userId: user.id,
  email: user.email,
  ip: req.ip
})''',
        ),
        UsageExample(
            name="Error Logging",
            description="Log errors with stack trace",
            code='''logger.error({
  message: 'Database query failed',
  error: err.message,
  stack: err.stack,
  query: sql
})''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="console.log everywhere",
            why="No structure, hard to search, no log levels",
            good="Use proper logger with levels",
        ),
        AntiPattern(
            bad="Logging passwords/tokens",
            why="Security breach",
            good="Sanitize sensitive data before logging",
        ),
        AntiPattern(
            bad="No log rotation",
            why="Fills disk, crashes server",
            good="Rotate daily or by size",
        ),
    ]

    file_structure: dict = {
        "backend/lib/logger.ts": "Logger configuration (Node.js)",
        "backend/lib/logger.py": "Logger configuration (Python)",
    }

    logger_ts: str = r'''// backend/lib/logger.ts
import winston from 'winston'
import DailyRotateFile from 'winston-daily-rotate-file'
import path from 'path'

// Custom format for console output
const consoleFormat = winston.format.combine(
  winston.format.colorize(),
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.printf(({ timestamp, level, message, ...meta }) => {
    const metaStr = Object.keys(meta).length ? JSON.stringify(meta, null, 2) : ''
    return `${timestamp} [${level}]: ${message} ${metaStr}`
  })
)

// JSON format for file output
const fileFormat = winston.format.combine(
  winston.format.timestamp(),
  winston.format.errors({ stack: true }),
  winston.format.json()
)

// Create transports
const transports: winston.transport[] = [
  // Console output
  new winston.transports.Console({
    format: consoleFormat,
    level: process.env.LOG_LEVEL || 'info',
  }),

  // Error logs - daily rotation
  new DailyRotateFile({
    filename: path.join('logs', 'error-%DATE%.log'),
    datePattern: 'YYYY-MM-DD',
    level: 'error',
    format: fileFormat,
    maxSize: '20m',
    maxFiles: '14d',
  }),

  // Combined logs - daily rotation
  new DailyRotateFile({
    filename: path.join('logs', 'combined-%DATE%.log'),
    datePattern: 'YYYY-MM-DD',
    format: fileFormat,
    maxSize: '20m',
    maxFiles: '14d',
  }),
]

// Create logger
export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: fileFormat,
  transports,
  exitOnError: false,
})

// Development logging
if (process.env.NODE_ENV !== 'production') {
  logger.debug('Logger initialized in development mode')
}

/**
 * Express middleware for request logging
 */
export function requestLogger(req: any, res: any, next: any) {
  const start = Date.now()

  // Log on response finish
  res.on('finish', () => {
    const duration = Date.now() - start

    logger.info({
      message: 'HTTP Request',
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration: `${duration}ms`,
      ip: req.ip,
      userAgent: req.get('user-agent'),
    })
  })

  next()
}

/**
 * Sanitize sensitive data before logging
 */
export function sanitizeForLog(data: any): any {
  const sensitive = ['password', 'token', 'secret', 'apiKey', 'accessToken', 'refreshToken']

  if (typeof data !== 'object' || data === null) {
    return data
  }

  const sanitized = { ...data }

  for (const key in sanitized) {
    if (sensitive.some(s => key.toLowerCase().includes(s))) {
      sanitized[key] = '***REDACTED***'
    } else if (typeof sanitized[key] === 'object') {
      sanitized[key] = sanitizeForLog(sanitized[key])
    }
  }

  return sanitized
}

// Example usage in app
/*
import { logger, requestLogger } from './lib/logger'

// Use request logging middleware
app.use(requestLogger)

// Log events
logger.info({ message: 'Server started', port: 3000 })

// Log errors
try {
  // ... code
} catch (error) {
  logger.error({
    message: 'Operation failed',
    error: error.message,
    stack: error.stack
  })
}
*/
'''

    logger_py: str = r'''# backend/lib/logger.py
import logging
import json
import sys
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pythonjsonlogger import jsonlogger
from typing import Any, Dict
import os

# Create logs directory
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Custom JSON formatter
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter with timestamp."""

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['logger'] = record.name

# Console formatter (human-readable)
class ConsoleFormatter(logging.Formatter):
    """Colored console formatter."""

    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)

def setup_logger(name: str = "app") -> logging.Logger:
    """Setup application logger."""

    logger = logging.getLogger(name)
    logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_format = ConsoleFormatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # File handler - JSON format with rotation
    file_handler = TimedRotatingFileHandler(
        filename=log_dir / "app.log",
        when="midnight",
        interval=1,
        backupCount=14,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_format = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s'
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # Error file handler - only errors
    error_handler = RotatingFileHandler(
        filename=log_dir / "error.log",
        maxBytes=20 * 1024 * 1024,  # 20MB
        backupCount=5,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_format)
    logger.addHandler(error_handler)

    return logger

# Create default logger
logger = setup_logger()

def sanitize_for_log(data: Any) -> Any:
    """Sanitize sensitive data before logging."""
    sensitive_keys = ['password', 'token', 'secret', 'api_key', 'access_token', 'refresh_token']

    if not isinstance(data, dict):
        return data

    sanitized = data.copy()

    for key in sanitized:
        if any(s in key.lower() for s in sensitive_keys):
            sanitized[key] = "***REDACTED***"
        elif isinstance(sanitized[key], dict):
            sanitized[key] = sanitize_for_log(sanitized[key])

    return sanitized

# FastAPI middleware for request logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all HTTP requests."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration = (time.time() - start_time) * 1000  # ms

        # Log request
        logger.info(
            "HTTP Request",
            extra={
                "method": request.method,
                "url": str(request.url),
                "status_code": response.status_code,
                "duration_ms": f"{duration:.2f}",
                "client_ip": request.client.host,
                "user_agent": request.headers.get("user-agent"),
            }
        )

        return response

# Example usage
"""
from backend.lib.logger import logger, RequestLoggingMiddleware

# FastAPI app
app = FastAPI()
app.add_middleware(RequestLoggingMiddleware)

# Log events
logger.info("Server started", extra={"port": 8000})

# Log with context
logger.info(
    "User logged in",
    extra={
        "user_id": user.id,
        "email": user.email,
        "ip": request.client.host
    }
)

# Log errors
try:
    # ... code
except Exception as e:
    logger.error(
        "Operation failed",
        extra={"error": str(e)},
        exc_info=True  # Include stack trace
    )
"""
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "backend/lib/logger.ts": self.logger_ts,
            "backend/lib/logger.py": self.logger_py,
        }
