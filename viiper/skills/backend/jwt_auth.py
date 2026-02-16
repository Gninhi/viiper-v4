"""
Premium JWT Authentication Skill.

World-class JWT authentication patterns for Node.js and Python.
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


class JWTAuthenticationSkill(Skill):
    """
    JWT authentication implementation patterns.

    Features:
    - Token generation and validation
    - Access and refresh token patterns
    - Secure password hashing
    - Express.js middleware
    - FastAPI dependency injection
    - Token expiration handling
    - Environment-based secrets
    - Error handling
    """

    metadata: SkillMetadata = SkillMetadata(
        name="JWT Authentication",
        slug="jwt-authentication",
        category=SkillCategory.BACKEND_AUTH,
        difficulty=SkillDifficulty.ADVANCED,
        tags=["jwt", "authentication", "security", "express", "fastapi", "node", "python"],
        estimated_time_minutes=30,
        description="Production-ready JWT authentication with access/refresh tokens",
    )

    dependencies: list = [
        Dependency(
            name="jsonwebtoken",
            version="^9.0.2",
            package_manager="npm",
            reason="JWT signing and verification (Node.js)",
        ),
        Dependency(
            name="bcrypt",
            version="^5.1.1",
            package_manager="npm",
            reason="Password hashing (Node.js)",
        ),
        Dependency(
            name="python-jose[cryptography]",
            version="^3.3.0",
            package_manager="pip",
            reason="JWT signing and verification (Python)",
        ),
        Dependency(
            name="passlib[bcrypt]",
            version="^1.7.4",
            package_manager="pip",
            reason="Password hashing (Python)",
        ),
    ]

    best_practices: list = [
        BestPractice(
            title="Use Refresh Tokens",
            description="Short-lived access tokens + long-lived refresh tokens",
            code_reference="access: 15min, refresh: 7days",
            benefit="Security + good UX, limit damage if token stolen",
        ),
        BestPractice(
            title="Store Secret in Environment",
            description="Never hardcode JWT secret",
            code_reference="process.env.JWT_SECRET",
            benefit="Security, different secrets per environment",
        ),
        BestPractice(
            title="Hash Passwords Properly",
            description="Use bcrypt with salt rounds >= 10",
            code_reference="bcrypt.hash(password, 12)",
            benefit="Protection against rainbow tables",
        ),
        BestPractice(
            title="Validate Token on Every Request",
            description="Middleware to check token validity",
            code_reference="authMiddleware",
            benefit="Consistent security enforcement",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Express JWT Middleware",
            description="Protect routes with JWT",
            code='''app.post('/api/protected', authenticateToken, (req, res) => {
  res.json({ user: req.user })
})''',
        ),
        UsageExample(
            name="FastAPI Dependency",
            description="Protect endpoints",
            code='''@app.get("/api/protected")
async def protected(user: User = Depends(get_current_user)):
    return {"user": user}''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Storing JWT secret in code",
            why="Security breach if code is leaked",
            good="Use environment variables",
        ),
        AntiPattern(
            bad="No token expiration",
            why="Stolen tokens valid forever",
            good="Short expiration + refresh pattern",
        ),
        AntiPattern(
            bad="Storing passwords in plain text",
            why="Catastrophic security breach",
            good="Always hash with bcrypt/argon2",
        ),
    ]

    file_structure: dict = {
        "backend/auth/jwt.ts": "JWT utilities (Node.js)",
        "backend/auth/jwt.py": "JWT utilities (Python)",
        "backend/middleware/auth.ts": "Auth middleware (Express)",
        "backend/dependencies/auth.py": "Auth dependencies (FastAPI)",
    }

    # Node.js/Express implementation
    jwt_ts_code: str = '''// backend/auth/jwt.ts
import jwt from 'jsonwebtoken'
import bcrypt from 'bcrypt'

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key'
const JWT_EXPIRES_IN = '15m'
const REFRESH_TOKEN_EXPIRES_IN = '7d'

export interface TokenPayload {
  userId: string
  email: string
}

export async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, 12)
}

export async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash)
}

export function generateAccessToken(payload: TokenPayload): string {
  return jwt.sign(payload, JWT_SECRET, { expiresIn: JWT_EXPIRES_IN })
}

export function generateRefreshToken(payload: TokenPayload): string {
  return jwt.sign(payload, JWT_SECRET, { expiresIn: REFRESH_TOKEN_EXPIRES_IN })
}

export function verifyToken(token: string): TokenPayload {
  return jwt.verify(token, JWT_SECRET) as TokenPayload
}
'''

    auth_middleware_code: str = '''// backend/middleware/auth.ts
import { Request, Response, NextFunction } from 'express'
import { verifyToken, TokenPayload } from '../auth/jwt'

declare global {
  namespace Express {
    interface Request {
      user?: TokenPayload
    }
  }
}

export function authenticateToken(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers['authorization']
  const token = authHeader && authHeader.split(' ')[1]

  if (!token) {
    return res.status(401).json({ error: 'Access token required' })
  }

  try {
    const payload = verifyToken(token)
    req.user = payload
    next()
  } catch (error) {
    return res.status(403).json({ error: 'Invalid or expired token' })
  }
}
'''

    # Python/FastAPI implementation
    jwt_py_code: str = '''# backend/auth/jwt.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
'''

    auth_dependencies_code: str = '''# backend/dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.auth.jwt import verify_token
from jose import JWTError

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    token = credentials.credentials

    try:
        payload = verify_token(token)
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """Generate JWT authentication files."""
        return {
            "backend/auth/jwt.ts": self.jwt_ts_code,
            "backend/middleware/auth.ts": self.auth_middleware_code,
            "backend/auth/jwt.py": self.jwt_py_code,
            "backend/dependencies/auth.py": self.auth_dependencies_code,
        }
