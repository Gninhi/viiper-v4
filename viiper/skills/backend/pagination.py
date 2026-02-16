"""Premium Pagination Patterns Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class PaginationSkill(Skill):
    """Offset and cursor-based pagination patterns."""

    metadata: SkillMetadata = SkillMetadata(
        name="Pagination Patterns",
        slug="pagination",
        category=SkillCategory.BACKEND_API,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["pagination", "api", "performance", "prisma", "sqlalchemy"],
        estimated_time_minutes=20,
        description="Offset and cursor-based pagination with metadata and performance",
    )

    dependencies: list = [
        Dependency(name="prisma", version="^5.7.0", package_manager="npm", reason="ORM with pagination support"),
    ]

    best_practices: list = [
        BestPractice(
            title="Use Cursor Pagination for Large Datasets",
            description="More efficient than offset for infinite scroll",
            code_reference="cursor: { id: lastId }",
            benefit="O(1) lookup, no skipped records",
        ),
        BestPractice(
            title="Include Pagination Metadata",
            description="Return total count, page info",
            code_reference="{ data, total, page, pageSize, hasMore }",
            benefit="Client can build pagination UI",
        ),
        BestPractice(
            title="Set Max Page Size",
            description="Limit how many records per page",
            code_reference="Math.min(limit, 100)",
            benefit="Prevent DoS, manage resources",
        ),
        BestPractice(
            title="Use Indexes on Sort Columns",
            description="Database index on sortBy field",
            code_reference="@@index([createdAt])",
            benefit="Fast sorting, query performance",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Offset Pagination",
            description="Simple page-based pagination",
            code='''const { data, total } = await paginate(User, {
  page: 1,
  limit: 20,
  sortBy: 'createdAt',
  order: 'desc'
})''',
        ),
        UsageExample(
            name="Cursor Pagination",
            description="Efficient for large lists",
            code='''const { data, hasMore, nextCursor } = await cursorPaginate(Post, {
  cursor: lastId,
  limit: 20
})''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="No page size limit",
            why="Client can request 1M records, DoS",
            good="Max 100 records per page",
        ),
        AntiPattern(
            bad="Offset pagination on huge tables",
            why="OFFSET 1000000 is very slow",
            good="Use cursor pagination for scale",
        ),
        AntiPattern(
            bad="Not including total count",
            why="Can't build page numbers UI",
            good="Return metadata with totals",
        ),
    ]

    file_structure: dict = {
        "backend/lib/pagination.ts": "Pagination utilities (Node.js)",
        "backend/lib/pagination.py": "Pagination utilities (Python)",
    }

    pagination_ts: str = r'''// backend/lib/pagination.ts
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

interface OffsetPaginationParams {
  page?: number
  limit?: number
  sortBy?: string
  order?: 'asc' | 'desc'
}

interface OffsetPaginationResult<T> {
  data: T[]
  metadata: {
    total: number
    page: number
    pageSize: number
    totalPages: number
    hasNext: boolean
    hasPrev: boolean
  }
}

interface CursorPaginationParams {
  cursor?: string
  limit?: number
  sortBy?: string
  order?: 'asc' | 'desc'
}

interface CursorPaginationResult<T> {
  data: T[]
  metadata: {
    nextCursor: string | null
    hasMore: boolean
  }
}

/**
 * Offset pagination (page-based)
 * Good for: Small datasets, traditional page numbers UI
 * Example: /api/users?page=2&limit=20
 */
export async function offsetPaginate<T>(
  model: any,
  params: OffsetPaginationParams = {},
  where: any = {}
): Promise<OffsetPaginationResult<T>> {
  const page = Math.max(params.page || 1, 1)
  const limit = Math.min(params.limit || 20, 100) // Max 100
  const sortBy = params.sortBy || 'createdAt'
  const order = params.order || 'desc'

  const skip = (page - 1) * limit

  // Get total count
  const total = await model.count({ where })

  // Get paginated data
  const data = await model.findMany({
    where,
    skip,
    take: limit,
    orderBy: { [sortBy]: order },
  })

  const totalPages = Math.ceil(total / limit)

  return {
    data,
    metadata: {
      total,
      page,
      pageSize: limit,
      totalPages,
      hasNext: page < totalPages,
      hasPrev: page > 1,
    },
  }
}

/**
 * Cursor pagination (cursor-based)
 * Good for: Large datasets, infinite scroll, real-time feeds
 * Example: /api/posts?cursor=abc123&limit=20
 */
export async function cursorPaginate<T>(
  model: any,
  params: CursorPaginationParams = {},
  where: any = {}
): Promise<CursorPaginationResult<T>> {
  const limit = Math.min(params.limit || 20, 100) // Max 100
  const sortBy = params.sortBy || 'createdAt'
  const order = params.order || 'desc'

  // Build query
  const query: any = {
    where,
    take: limit + 1, // Fetch one extra to check if there's more
    orderBy: { [sortBy]: order },
  }

  // Add cursor if provided
  if (params.cursor) {
    query.cursor = { id: params.cursor }
    query.skip = 1 // Skip the cursor itself
  }

  // Fetch data
  const results = await model.findMany(query)

  // Check if there are more results
  const hasMore = results.length > limit
  const data = hasMore ? results.slice(0, limit) : results

  // Get next cursor (last item's ID)
  const nextCursor = hasMore && data.length > 0 ? data[data.length - 1].id : null

  return {
    data,
    metadata: {
      nextCursor,
      hasMore,
    },
  }
}

/**
 * Express middleware for pagination
 */
export function paginationMiddleware(req: any, res: any, next: any) {
  const page = parseInt(req.query.page as string) || 1
  const limit = Math.min(parseInt(req.query.limit as string) || 20, 100)
  const sortBy = req.query.sortBy as string || 'createdAt'
  const order = (req.query.order as 'asc' | 'desc') || 'desc'

  req.pagination = { page, limit, sortBy, order }
  next()
}

/**
 * Build pagination links for API responses
 */
export function buildPaginationLinks(
  baseUrl: string,
  page: number,
  totalPages: number,
  params: Record<string, any> = {}
): Record<string, string | null> {
  const buildUrl = (p: number) => {
    const query = new URLSearchParams({
      ...params,
      page: p.toString(),
    }).toString()
    return `${baseUrl}?${query}`
  }

  return {
    first: page > 1 ? buildUrl(1) : null,
    prev: page > 1 ? buildUrl(page - 1) : null,
    next: page < totalPages ? buildUrl(page + 1) : null,
    last: page < totalPages ? buildUrl(totalPages) : null,
  }
}
'''

    pagination_py: str = r'''# backend/lib/pagination.py
from typing import TypeVar, Generic, List, Optional, Dict, Any
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")

class OffsetPaginationMetadata(BaseModel):
    """Metadata for offset pagination."""
    total: int
    page: int
    page_size: int = Field(alias="pageSize")
    total_pages: int = Field(alias="totalPages")
    has_next: bool = Field(alias="hasNext")
    has_prev: bool = Field(alias="hasPrev")

    class Config:
        populate_by_name = True

class OffsetPaginationResult(BaseModel, Generic[T]):
    """Offset pagination result."""
    data: List[T]
    metadata: OffsetPaginationMetadata

class CursorPaginationMetadata(BaseModel):
    """Metadata for cursor pagination."""
    next_cursor: Optional[str] = Field(alias="nextCursor")
    has_more: bool = Field(alias="hasMore")

    class Config:
        populate_by_name = True

class CursorPaginationResult(BaseModel, Generic[T]):
    """Cursor pagination result."""
    data: List[T]
    metadata: CursorPaginationMetadata

async def offset_paginate(
    session: AsyncSession,
    model: Any,
    page: int = 1,
    limit: int = 20,
    sort_by: str = "created_at",
    order: str = "desc",
    filters: Optional[Dict] = None
) -> OffsetPaginationResult:
    """
    Offset pagination (page-based).

    Good for: Small datasets, traditional page numbers UI
    Example: /api/users?page=2&limit=20
    """
    page = max(page, 1)
    limit = min(limit, 100)  # Max 100 per page

    # Build base query
    stmt = select(model)

    # Apply filters
    if filters:
        for key, value in filters.items():
            stmt = stmt.where(getattr(model, key) == value)

    # Get total count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = await session.scalar(count_stmt)

    # Apply sorting
    order_by = getattr(model, sort_by)
    if order == "desc":
        order_by = order_by.desc()
    stmt = stmt.order_by(order_by)

    # Apply pagination
    offset = (page - 1) * limit
    stmt = stmt.offset(offset).limit(limit)

    # Execute query
    result = await session.execute(stmt)
    data = result.scalars().all()

    total_pages = (total + limit - 1) // limit  # Ceiling division

    return OffsetPaginationResult(
        data=data,
        metadata=OffsetPaginationMetadata(
            total=total,
            page=page,
            pageSize=limit,
            totalPages=total_pages,
            hasNext=page < total_pages,
            hasPrev=page > 1,
        )
    )

async def cursor_paginate(
    session: AsyncSession,
    model: Any,
    cursor: Optional[str] = None,
    limit: int = 20,
    sort_by: str = "created_at",
    order: str = "desc",
    filters: Optional[Dict] = None
) -> CursorPaginationResult:
    """
    Cursor pagination (cursor-based).

    Good for: Large datasets, infinite scroll, real-time feeds
    Example: /api/posts?cursor=abc123&limit=20
    """
    limit = min(limit, 100)  # Max 100 per page

    # Build base query
    stmt = select(model)

    # Apply filters
    if filters:
        for key, value in filters.items():
            stmt = stmt.where(getattr(model, key) == value)

    # Apply cursor
    if cursor:
        stmt = stmt.where(getattr(model, "id") > cursor)

    # Apply sorting
    order_by = getattr(model, sort_by)
    if order == "desc":
        order_by = order_by.desc()
    stmt = stmt.order_by(order_by)

    # Fetch limit + 1 to check if there are more
    stmt = stmt.limit(limit + 1)

    # Execute query
    result = await session.execute(stmt)
    results = result.scalars().all()

    # Check if there are more results
    has_more = len(results) > limit
    data = results[:limit] if has_more else results

    # Get next cursor
    next_cursor = str(data[-1].id) if has_more and data else None

    return CursorPaginationResult(
        data=data,
        metadata=CursorPaginationMetadata(
            nextCursor=next_cursor,
            hasMore=has_more,
        )
    )

class PaginationParams(BaseModel):
    """Query parameters for pagination."""
    page: int = Field(1, ge=1, description="Page number")
    limit: int = Field(20, ge=1, le=100, description="Items per page")
    sort_by: str = Field("created_at", description="Sort field")
    order: str = Field("desc", pattern="^(asc|desc)$", description="Sort order")

def build_pagination_links(
    base_url: str,
    page: int,
    total_pages: int,
    params: Dict[str, Any] = None
) -> Dict[str, Optional[str]]:
    """Build pagination links for API responses."""
    params = params or {}

    def build_url(p: int) -> str:
        query_params = {**params, "page": p}
        query_string = "&".join(f"{k}={v}" for k, v in query_params.items())
        return f"{base_url}?{query_string}"

    return {
        "first": build_url(1) if page > 1 else None,
        "prev": build_url(page - 1) if page > 1 else None,
        "next": build_url(page + 1) if page < total_pages else None,
        "last": build_url(total_pages) if page < total_pages else None,
    }
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "backend/lib/pagination.ts": self.pagination_ts,
            "backend/lib/pagination.py": self.pagination_py,
        }
