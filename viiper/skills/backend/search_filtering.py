"""Premium Search & Filtering Patterns Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class SearchFilteringSkill(Skill):
    """Advanced search and filtering patterns for APIs and Databases."""

    metadata: SkillMetadata = SkillMetadata(
        name="Search & Filtering Patterns",
        slug="search-filtering",
        category=SkillCategory.BACKEND_API,
        difficulty=SkillDifficulty.ADVANCED,
        tags=["search", "filtering", "full-text-search", "performance", "prisma", "sqlalchemy"],
        estimated_time_minutes=45,
        description="Comprehensive search and filtering patterns including full-text search and dynamic query builders.",
    )

    dependencies: list = [
        Dependency(name="prisma", version="^5.7.0", package_manager="npm", reason="ORM with robust filtering support"),
        Dependency(name="sqlalchemy", version="^2.0.0", package_manager="pip", reason="Python ORM for dynamic queries"),
    ]

    best_practices: list = [
        BestPractice(
            title="Use GIN Indexes for Full-Text Search",
            description="Enable fast text searching in Postgres using GIN indexes on tsvector columns.",
            code_reference="CREATE INDEX idx_fts ON posts USING GIN (to_tsvector('english', title || ' ' || content));",
            benefit="Sub-second search on millions of rows.",
        ),
        BestPractice(
            title="Implement Case-Insensitive Search",
            description="Use 'mode: insensitive' in Prisma or 'ilike' in SQLAlchemy.",
            code_reference="where: { name: { contains: 'query', mode: 'insensitive' } }",
            benefit="Better UX as users don't need to match casing.",
        ),
        BestPractice(
            title="Dynamic Query Building",
            description="Build queries dynamically based on provided filter objects to avoid over-fetching.",
            code_reference="if (params.status) where.status = params.status;",
            benefit="Flexible API that handles optional filters efficiently.",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Prisma Complex Filtering",
            description="Combining multiple optional filters with logical AND.",
            code='''const results = await prisma.product.findMany({
  where: {
    AND: [
      { category: 'electronics' },
      { price: { gte: 100, lte: 500 } },
      { name: { contains: 'search', mode: 'insensitive' } }
    ]
  }
});''',
        ),
        UsageExample(
            name="SQLAlchemy Dynamic Filter",
            description="Using a dictionary to build a SQLAlchemy filter set.",
            code='''filters = {"status": "active", "category_id": 5}
query = select(User).filter_by(**filters)
results = await session.execute(query)''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Filtering in-memory (JS/Python level)",
            why="Inefficient for large datasets; fetches all rows before filtering.",
            good="Push filters down to the database using WHERE clauses.",
        ),
        AntiPattern(
            bad="SQL Injection in raw search queries",
            why="Unsafe concatenating user input into search strings.",
            good="Use parameterized queries or ORM search abstractions.",
        ),
    ]

    file_structure: dict = {
        "backend/lib/search.ts": "Search and filtering utilities (Node.js/Prisma)",
        "backend/lib/search.py": "Search and filtering utilities (Python/SQLAlchemy)",
    }

    search_ts: str = r'''// backend/lib/search.ts
import { Prisma } from '@prisma/client'

/**
 * Build a dynamic Prisma 'where' object from filter parameters.
 */
export function buildSearchQuery(params: Record<string, any>) {
  const where: Prisma.UserWhereInput = {}
  const { q, status, role, fromDate, toDate } = params

  if (q) {
    where.OR = [
      { name: { contains: q, mode: 'insensitive' } },
      { email: { contains: q, mode: 'insensitive' } }
    ]
  }

  if (status) where.status = status
  if (role) where.role = role

  if (fromDate || toDate) {
    where.createdAt = {
      ...(fromDate && { gte: new Date(fromDate) }),
      ...(toDate && { lte: new Date(toDate) })
    }
  }

  return where
}

/**
 * Specialized Full-Text Search using Postgres raw SQL (if needed)
 */
export async function fullTextSearch(prisma: any, tableName: string, query: string) {
  return prisma.$queryRawUnsafe(
    `SELECT * FROM "${tableName}" 
     WHERE to_tsvector('english', title || ' ' || content) @@ plainto_tsquery('english', $1)
     ORDER BY ts_rank(to_tsvector('english', title || ' ' || content), plainto_tsquery('english', $1)) DESC`,
    query
  )
}
'''

    search_py: str = r'''# backend/lib/search.py
from typing import Any, Dict, List, Optional
from sqlalchemy import select, or_, and_, text
from sqlalchemy.sql import Select

def apply_filters(query: Select, model: Any, filters: Dict[str, Any]) -> Select:
    """
    Dynamically applies filters to a SQLAlchemy select statement.
    """
    for key, value in filters.items():
        if value is None:
            continue
            
        if hasattr(model, key):
            column = getattr(model, key)
            if isinstance(value, list):
                query = query.where(column.in_(value))
            elif isinstance(value, str) and "%" in value:
                query = query.where(column.ilike(value))
            else:
                query = query.where(column == value)
                
    return query

def build_fts_query(query: Select, model: Any, search_text: str, columns: List[str]) -> Select:
    """
    Applies simple full-text search overlay across multiple columns.
    """
    if not search_text:
        return query
        
    conditions = []
    for col_name in columns:
        if hasattr(model, col_name):
            conditions.append(getattr(model, col_name).ilike(f"%{search_text}%"))
            
    return query.where(or_(*conditions))
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "backend/lib/search.ts": self.search_ts,
            "backend/lib/search.py": self.search_py,
        }
