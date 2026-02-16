"""Premium Database Models Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class DatabaseModelsSkill(Skill):
    """Database model patterns with Prisma, TypeORM, and SQLAlchemy."""

    metadata: SkillMetadata = SkillMetadata(
        name="Database Models & ORM Patterns",
        slug="database-models",
        category=SkillCategory.BACKEND_DATABASE,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["database", "orm", "prisma", "typeorm", "sqlalchemy", "models"],
        estimated_time_minutes=30,
        description="Production database models with Prisma, TypeORM, and SQLAlchemy",
    )

    dependencies: list = [
        Dependency(name="@prisma/client", version="^5.8.0", package_manager="npm", reason="Prisma ORM (Node.js)"),
        Dependency(name="typeorm", version="^0.3.19", package_manager="npm", reason="TypeORM (Node.js)"),
        Dependency(name="sqlalchemy", version="^2.0.25", package_manager="pip", reason="SQLAlchemy ORM (Python)"),
    ]

    best_practices: list = [
        BestPractice(
            title="Use Migrations",
            description="Never modify database schema directly",
            code_reference="prisma migrate dev",
            benefit="Version control for database, rollback support",
        ),
        BestPractice(
            title="Index Foreign Keys",
            description="Add indexes to foreign key columns",
            code_reference="@@index([userId])",
            benefit="Query performance",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Prisma Schema",
            description="User model with relations",
            code='''model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  createdAt DateTime @default(now())

  @@index([authorId])
}''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="No timestamps",
            why="Can't track when records created/modified",
            good="Always include createdAt/updatedAt",
        ),
    ]

    file_structure: dict = {
        "prisma/schema.prisma": "Prisma schema",
        "backend/models/user.entity.ts": "TypeORM entity",
        "backend/models/user.py": "SQLAlchemy model",
    }

    prisma_schema: str = '''// prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String
  password  String
  role      Role     @default(USER)
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)
  authorId  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([authorId])
  @@index([published])
}

model Profile {
  id     String @id @default(cuid())
  bio    String?
  avatar String?
  user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)
  userId String @unique
}

enum Role {
  USER
  ADMIN
}
'''

    typeorm_entity: str = '''// backend/models/user.entity.ts
import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn, OneToMany } from 'typeorm'
import { Post } from './post.entity'

export enum UserRole {
  USER = 'user',
  ADMIN = 'admin'
}

@Entity('users')
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string

  @Column({ unique: true })
  email: string

  @Column()
  name: string

  @Column()
  password: string

  @Column({
    type: 'enum',
    enum: UserRole,
    default: UserRole.USER
  })
  role: UserRole

  @OneToMany(() => Post, post => post.author)
  posts: Post[]

  @CreateDateColumn()
  createdAt: Date

  @UpdateDateColumn()
  updatedAt: Date
}
'''

    sqlalchemy_model: str = '''# backend/models/user.py
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base
import enum

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Post(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=False, index=True)
    author_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), index=True)

    author = relationship("User", back_populates="posts")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "prisma/schema.prisma": self.prisma_schema,
            "backend/models/user.entity.ts": self.typeorm_entity,
            "backend/models/user.py": self.sqlalchemy_model,
        }
