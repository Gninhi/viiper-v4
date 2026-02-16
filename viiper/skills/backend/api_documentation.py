"""Premium API Documentation Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class APIDocumentationSkill(Skill):
    """Interactive API documentation with Swagger/OpenAPI."""

    metadata: SkillMetadata = SkillMetadata(
        name="API Documentation",
        slug="api-documentation",
        category=SkillCategory.BACKEND_API,
        difficulty=SkillDifficulty.BEGINNER,
        tags=["documentation", "swagger", "openapi", "api-docs", "redoc"],
        estimated_time_minutes=20,
        description="Auto-generated API docs with Swagger UI and OpenAPI specification",
    )

    dependencies: list = [
        Dependency(name="swagger-ui-express", version="^5.0.0", package_manager="npm", reason="Swagger UI (Express)"),
        Dependency(name="swagger-jsdoc", version="^6.2.8", package_manager="npm", reason="Generate OpenAPI from JSDoc"),
    ]

    best_practices: list = [
        BestPractice(
            title="Document All Endpoints",
            description="Every route should have OpenAPI spec",
            code_reference="@swagger comments or decorators",
            benefit="Complete, accurate documentation",
        ),
        BestPractice(
            title="Include Request/Response Examples",
            description="Show example JSON payloads",
            code_reference="examples in schema",
            benefit="Developers understand API faster",
        ),
        BestPractice(
            title="Version Your API",
            description="Track API versions in OpenAPI spec",
            code_reference="version: '1.0.0'",
            benefit="Backward compatibility tracking",
        ),
        BestPractice(
            title="Add Authentication Docs",
            description="Document JWT, API keys, etc.",
            code_reference="securitySchemes in OpenAPI",
            benefit="Clear auth requirements",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="JSDoc API Comment",
            description="Document Express route",
            code='''/**
 * @swagger
 * /api/users:
 *   get:
 *     summary: List all users
 *     responses:
 *       200:
 *         description: Success
 */''',
        ),
        UsageExample(
            name="FastAPI Auto-Docs",
            description="Automatic docs from type hints",
            code='''@app.get("/api/users", response_model=List[UserResponse])
async def get_users():
    return await db.users.find_all()''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="No API documentation",
            why="Developers waste time figuring out API",
            good="Auto-generated docs from code",
        ),
        AntiPattern(
            bad="Outdated documentation",
            why="Docs don't match actual API",
            good="Generate docs from code",
        ),
    ]

    file_structure: dict = {
        "backend/lib/swagger.ts": "Swagger configuration (Express)",
        "backend/lib/openapi.py": "OpenAPI configuration (FastAPI)",
    }

    swagger_config_ts: str = r'''// backend/lib/swagger.ts
import swaggerJsdoc from 'swagger-jsdoc'
import swaggerUi from 'swagger-ui-express'
import { Express } from 'express'

const swaggerOptions: swaggerJsdoc.Options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'API Documentation',
      version: '1.0.0',
      description: 'Comprehensive API documentation with examples',
      contact: {
        name: 'API Support',
        email: 'support@example.com',
      },
    },
    servers: [
      {
        url: process.env.API_URL || 'http://localhost:3000',
        description: 'Development server',
      },
    ],
    components: {
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT',
          description: 'Enter your JWT token',
        },
      },
      schemas: {
        User: {
          type: 'object',
          properties: {
            id: { type: 'string', format: 'uuid' },
            email: { type: 'string', format: 'email' },
            name: { type: 'string' },
            role: { type: 'string', enum: ['USER', 'ADMIN'] },
            createdAt: { type: 'string', format: 'date-time' },
          },
          required: ['id', 'email', 'name'],
        },
        Error: {
          type: 'object',
          properties: {
            error: { type: 'string' },
            details: { type: 'array', items: { type: 'object' } },
          },
        },
      },
    },
    security: [
      {
        bearerAuth: [],
      },
    ],
  },
  apis: ['./backend/routes/*.ts', './backend/controllers/*.ts'],
}

const swaggerSpec = swaggerJsdoc(swaggerOptions)

/**
 * Setup Swagger UI
 */
export function setupSwagger(app: Express) {
  // Swagger UI
  app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec, {
    customCss: '.swagger-ui .topbar { display: none }',
    customSiteTitle: 'API Documentation',
  }))

  // OpenAPI JSON
  app.get('/api-docs.json', (req, res) => {
    res.setHeader('Content-Type', 'application/json')
    res.send(swaggerSpec)
  })

  console.log('📚 API Documentation available at /api-docs')
}

// Example route with JSDoc:
/**
 * @swagger
 * /api/users:
 *   get:
 *     summary: List all users
 *     description: Retrieve a list of all users with pagination
 *     tags:
 *       - Users
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *           default: 1
 *         description: Page number
 *       - in: query
 *         name: limit
 *         schema:
 *           type: integer
 *           default: 20
 *         description: Items per page
 *     responses:
 *       200:
 *         description: List of users
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 data:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/User'
 *                 metadata:
 *                   type: object
 *                   properties:
 *                     total: { type: integer }
 *                     page: { type: integer }
 *                     pageSize: { type: integer }
 *       401:
 *         description: Unauthorized
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Error'
 *     security:
 *       - bearerAuth: []
 */

/**
 * @swagger
 * /api/users/{id}:
 *   get:
 *     summary: Get user by ID
 *     tags:
 *       - Users
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *         description: User ID
 *     responses:
 *       200:
 *         description: User details
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/User'
 *       404:
 *         description: User not found
 *   put:
 *     summary: Update user
 *     tags:
 *       - Users
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: User ID
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               name: { type: string }
 *               email: { type: string, format: email }
 *     responses:
 *       200:
 *         description: User updated
 *       400:
 *         description: Invalid input
 */
'''

    openapi_config_py: str = r'''# backend/lib/openapi.py
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from typing import Dict, Any

def custom_openapi(app: FastAPI) -> Dict[str, Any]:
    """
    Customize OpenAPI schema.

    FastAPI auto-generates OpenAPI docs from type hints.
    This function customizes the generated schema.
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="API Documentation",
        version="1.0.0",
        description="""
## Comprehensive API Documentation

This API provides a complete backend for your application with:

* **Authentication**: JWT-based auth with access/refresh tokens
* **CRUD Operations**: Full create, read, update, delete for resources
* **File Uploads**: Secure file uploads with validation
* **Real-time**: WebSocket support for live updates
* **Pagination**: Efficient pagination for large datasets

## Authentication

Most endpoints require authentication. Include your JWT token in the Authorization header:

```
Authorization: Bearer <your-token>
```

Get a token by logging in at `/api/auth/login`.

## Rate Limiting

API endpoints are rate-limited to prevent abuse:
- Authentication endpoints: 5 requests per 15 minutes
- Read operations: 60 requests per minute
- Write operations: 10 requests per minute

## Support

For questions or issues, contact support@example.com
        """,
        routes=app.routes,
        contact={
            "name": "API Support",
            "email": "support@example.com",
        },
        servers=[
            {
                "url": "http://localhost:8000",
                "description": "Development server"
            },
            {
                "url": "https://api.example.com",
                "description": "Production server"
            },
        ],
    )

    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT access token"
        }
    }

    # Add security globally
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            # Skip health checks and auth endpoints
            if path.startswith("/health") or path.startswith("/api/auth"):
                continue

            openapi_schema["paths"][path][method]["security"] = [
                {"bearerAuth": []}
            ]

    # Add tags metadata
    openapi_schema["tags"] = [
        {
            "name": "Authentication",
            "description": "User authentication and authorization"
        },
        {
            "name": "Users",
            "description": "User management operations"
        },
        {
            "name": "Posts",
            "description": "Blog post operations"
        },
        {
            "name": "Health",
            "description": "System health checks"
        },
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

def setup_api_docs(app: FastAPI):
    """Setup API documentation."""
    app.openapi = lambda: custom_openapi(app)

    # API docs are automatically available at:
    # - /docs (Swagger UI)
    # - /redoc (ReDoc)
    # - /openapi.json (OpenAPI JSON schema)

    print("📚 API Documentation available at:")
    print("  - Swagger UI: /docs")
    print("  - ReDoc: /redoc")
    print("  - OpenAPI JSON: /openapi.json")

# Example route with documentation
"""
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List

class UserResponse(BaseModel):
    \"\"\"User response model.\"\"\"
    id: str
    email: str
    name: str
    role: str
    created_at: str

    class Config:
        from_attributes = True

@app.get(
    "/api/users",
    response_model=List[UserResponse],
    tags=["Users"],
    summary="List all users",
    description="Retrieve a paginated list of all users. Requires authentication.",
    responses={
        200: {
            "description": "List of users",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "id": "123e4567-e89b-12d3-a456-426614174000",
                                "email": "user@example.com",
                                "name": "John Doe",
                                "role": "USER",
                                "created_at": "2024-01-15T10:30:00Z"
                            }
                        ],
                        "metadata": {
                            "total": 100,
                            "page": 1,
                            "pageSize": 20
                        }
                    }
                }
            }
        },
        401: {"description": "Unauthorized - Invalid or missing token"},
        429: {"description": "Too many requests - Rate limit exceeded"}
    }
)
async def get_users(
    page: int = 1,
    limit: int = 20,
    user = Depends(get_current_user)
):
    \"\"\"Get all users with pagination.\"\"\"
    pass
"""
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "backend/lib/swagger.ts": self.swagger_config_ts,
            "backend/lib/openapi.py": self.openapi_config_py,
        }
