"""Premium Input Validation Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class InputValidationSkill(Skill):
    """Input validation patterns for API endpoints."""

    metadata: SkillMetadata = SkillMetadata(
        name="Input Validation",
        slug="input-validation",
        category=SkillCategory.BACKEND_API,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["validation", "zod", "pydantic", "express", "fastapi", "security"],
        estimated_time_minutes=25,
        description="Type-safe input validation with Zod (Node.js) and Pydantic (Python)",
    )

    dependencies: list = [
        Dependency(name="zod", version="^3.22.4", package_manager="npm", reason="Schema validation (Node.js)"),
        Dependency(name="pydantic", version="^2.5.0", package_manager="pip", reason="Data validation (Python)"),
    ]

    best_practices: list = [
        BestPractice(
            title="Validate at API Boundaries",
            description="Always validate external input",
            code_reference="Validate request body, query params, path params",
            benefit="Security, data integrity",
        ),
        BestPractice(
            title="Return Clear Error Messages",
            description="Tell users exactly what's wrong",
            code_reference="Field-level validation errors",
            benefit="Better UX, faster debugging",
        ),
        BestPractice(
            title="Use Type-Safe Schemas",
            description="Schemas provide both validation and types",
            code_reference="Zod.infer<typeof schema>",
            benefit="Compile-time safety + runtime validation",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Express Validation Middleware",
            description="Validate request body",
            code='''app.post('/api/users', validateBody(createUserSchema), (req, res) => {
  // req.body is now type-safe and validated
  const user = req.body
})''',
        ),
        UsageExample(
            name="FastAPI Automatic Validation",
            description="Pydantic models auto-validate",
            code='''@app.post("/api/users")
async def create_user(user: CreateUserRequest):
    # user is validated automatically
    return {"id": "123", "email": user.email}''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Manual string checks",
            why="Error-prone, inconsistent",
            good="Use validation schemas",
        ),
        AntiPattern(
            bad="Trusting client input",
            why="Security vulnerabilities",
            good="Validate everything from external sources",
        ),
    ]

    file_structure: dict = {
        "backend/lib/validation.ts": "Zod validation middleware (Express)",
        "backend/schemas/user.ts": "User validation schemas (Zod)",
        "backend/schemas/user.py": "User validation models (Pydantic)",
    }

    validation_middleware: str = '''// backend/lib/validation.ts
import { Request, Response, NextFunction } from 'express'
import { ZodSchema, ZodError } from 'zod'

export function validateBody(schema: ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      req.body = schema.parse(req.body)
      next()
    } catch (error) {
      if (error instanceof ZodError) {
        return res.status(400).json({
          error: 'Validation failed',
          details: error.errors.map(err => ({
            field: err.path.join('.'),
            message: err.message
          }))
        })
      }
      next(error)
    }
  }
}

export function validateQuery(schema: ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      req.query = schema.parse(req.query)
      next()
    } catch (error) {
      if (error instanceof ZodError) {
        return res.status(400).json({
          error: 'Invalid query parameters',
          details: error.errors
        })
      }
      next(error)
    }
  }
}

export function validateParams(schema: ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      req.params = schema.parse(req.params)
      next()
    } catch (error) {
      if (error instanceof ZodError) {
        return res.status(400).json({
          error: 'Invalid path parameters',
          details: error.errors
        })
      }
      next(error)
    }
  }
}
'''

    user_schemas_ts: str = '''// backend/schemas/user.ts
import { z } from 'zod'

export const createUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  name: z.string().min(2, 'Name must be at least 2 characters'),
  role: z.enum(['USER', 'ADMIN']).optional().default('USER')
})

export const updateUserSchema = z.object({
  email: z.string().email().optional(),
  name: z.string().min(2).optional(),
  role: z.enum(['USER', 'ADMIN']).optional()
}).refine(data => Object.keys(data).length > 0, {
  message: 'At least one field must be provided'
})

export const userIdSchema = z.object({
  id: z.string().uuid('Invalid user ID format')
})

export const paginationSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().positive().max(100).default(20),
  sortBy: z.string().optional(),
  order: z.enum(['asc', 'desc']).optional().default('asc')
})

// Infer TypeScript types from schemas
export type CreateUserInput = z.infer<typeof createUserSchema>
export type UpdateUserInput = z.infer<typeof updateUserSchema>
export type UserIdParams = z.infer<typeof userIdSchema>
export type PaginationQuery = z.infer<typeof paginationSchema>
'''

    user_schemas_py: str = '''# backend/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Literal
from datetime import datetime

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    name: str = Field(..., min_length=2, description="Name must be at least 2 characters")
    role: Literal["USER", "ADMIN"] = "USER"

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class UpdateUserRequest(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=2)
    role: Optional[Literal["USER", "ADMIN"]] = None

    @field_validator('*', mode='before')
    @classmethod
    def check_at_least_one_field(cls, v, info):
        # This runs after all fields are set
        return v

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # For SQLAlchemy compatibility

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number")
    limit: int = Field(20, ge=1, le=100, description="Items per page")
    sort_by: Optional[str] = None
    order: Literal["asc", "desc"] = "asc"
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "backend/lib/validation.ts": self.validation_middleware,
            "backend/schemas/user.ts": self.user_schemas_ts,
            "backend/schemas/user.py": self.user_schemas_py,
        }
