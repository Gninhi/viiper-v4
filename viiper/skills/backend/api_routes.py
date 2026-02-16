"""
Premium REST API Routes Skill.

Best practices for building RESTful APIs with Express and FastAPI.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill,
    SkillMetadata,
    SkillCategory,
    SkillDifficulty,
    Dependency,
    BestPractice,
    UsageExample,
    AntiPattern,
)


class RESTAPIRoutesSkill(Skill):
    """REST API route patterns for Express and FastAPI."""

    metadata: SkillMetadata = SkillMetadata(
        name="REST API Routes",
        slug="rest-api-routes",
        category=SkillCategory.BACKEND_API,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["rest", "api", "express", "fastapi", "routes", "endpoints"],
        estimated_time_minutes=25,
        description="RESTful API patterns with Express.js and FastAPI",
    )

    dependencies: list = [
        Dependency(name="express", version="^4.18.2", package_manager="npm", reason="Web framework (Node.js)"),
        Dependency(name="fastapi", version="^0.109.0", package_manager="pip", reason="Web framework (Python)"),
        Dependency(name="pydantic", version="^2.5.0", package_manager="pip", reason="Validation (Python)"),
    ]

    best_practices: list = [
        BestPractice(
            title="Use HTTP Status Codes Correctly",
            description="200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Server Error",
            code_reference="res.status(201).json()",
            benefit="Clear communication of operation result",
        ),
        BestPractice(
            title="Validate Input Data",
            description="Always validate request bodies and params",
            code_reference="Pydantic models / Zod schemas",
            benefit="Prevent invalid data, clear error messages",
        ),
        BestPractice(
            title="Use Consistent Response Format",
            description="Standard shape for all responses",
            code_reference='{ "data": {}, "error": null }',
            benefit="Predictable API, easier client integration",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Express CRUD Routes",
            description="Full CRUD for resource",
            code='''// GET /api/users - List all
app.get('/api/users', async (req, res) => {
  const users = await db.user.findMany()
  res.json({ data: users })
})

// POST /api/users - Create
app.post('/api/users', async (req, res) => {
  const user = await db.user.create({ data: req.body })
  res.status(201).json({ data: user })
})

// PUT /api/users/:id - Update
app.put('/api/users/:id', async (req, res) => {
  const user = await db.user.update({
    where: { id: req.params.id },
    data: req.body
  })
  res.json({ data: user })
})

// DELETE /api/users/:id - Delete
app.delete('/api/users/:id', async (req, res) => {
  await db.user.delete({ where: { id: req.params.id } })
  res.status(204).send()
})''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Using GET for mutations",
            why="Not RESTful, breaks caching, unsafe",
            good="POST/PUT/DELETE for mutations",
        ),
        AntiPattern(
            bad="No error handling",
            why="Server crashes on errors, poor UX",
            good="Try-catch with proper error responses",
        ),
    ]

    file_structure: dict = {
        "backend/routes/users.ts": "User routes (Express)",
        "backend/routers/users.py": "User router (FastAPI)",
    }

    express_routes_code: str = '''// backend/routes/users.ts
import { Router } from 'express'
import { z } from 'zod'

const router = Router()

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
  password: z.string().min(8),
})

// GET /api/users - List users
router.get('/', async (req, res, next) => {
  try {
    const users = await db.user.findMany({
      select: { id: true, email: true, name: true }
    })
    res.json({ data: users })
  } catch (error) {
    next(error)
  }
})

// GET /api/users/:id - Get single user
router.get('/:id', async (req, res, next) => {
  try {
    const user = await db.user.findUnique({
      where: { id: req.params.id }
    })
    if (!user) {
      return res.status(404).json({ error: 'User not found' })
    }
    res.json({ data: user })
  } catch (error) {
    next(error)
  }
})

// POST /api/users - Create user
router.post('/', async (req, res, next) => {
  try {
    const validatedData = createUserSchema.parse(req.body)
    const user = await db.user.create({ data: validatedData })
    res.status(201).json({ data: user })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ error: error.errors })
    }
    next(error)
  }
})

// PUT /api/users/:id - Update user
router.put('/:id', async (req, res, next) => {
  try {
    const user = await db.user.update({
      where: { id: req.params.id },
      data: req.body
    })
    res.json({ data: user })
  } catch (error) {
    next(error)
  }
})

// DELETE /api/users/:id - Delete user
router.delete('/:id', async (req, res, next) => {
  try {
    await db.user.delete({ where: { id: req.params.id } })
    res.status(204).send()
  } catch (error) {
    next(error)
  }
})

export default router
'''

    fastapi_router_code: str = '''# backend/routers/users.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List

router = APIRouter(prefix="/api/users", tags=["users"])

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str

# GET /api/users - List users
@router.get("/", response_model=List[UserResponse])
async def list_users():
    users = await db.user.find_many()
    return users

# GET /api/users/{user_id} - Get single user
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = await db.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# POST /api/users - Create user
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    user = await db.user.create(data=user_data.dict())
    return user

# PUT /api/users/{user_id} - Update user
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_data: UserCreate):
    user = await db.user.update(
        where={"id": user_id},
        data=user_data.dict(exclude_unset=True)
    )
    return user

# DELETE /api/users/{user_id} - Delete user
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    await db.user.delete(where={"id": user_id})
    return None
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "backend/routes/users.ts": self.express_routes_code,
            "backend/routers/users.py": self.fastapi_router_code,
        }
