"""Premium Caching Strategies Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class CachingSkill(Skill):
    """Redis and in-memory caching patterns."""

    metadata: SkillMetadata = SkillMetadata(
        name="Caching Strategies",
        slug="caching",
        category=SkillCategory.BACKEND_API,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["caching", "redis", "performance", "optimization", "express", "fastapi"],
        estimated_time_minutes=25,
        description="Redis and in-memory caching with TTL, invalidation, and patterns",
    )

    dependencies: list = [
        Dependency(name="redis", version="^4.6.11", package_manager="npm", reason="Redis client (Node.js)"),
        Dependency(name="redis", version="^5.0.1", package_manager="pip", reason="Redis client (Python)"),
        Dependency(name="aioredis", version="^2.0.1", package_manager="pip", reason="Async Redis for FastAPI"),
    ]

    best_practices: list = [
        BestPractice(
            title="Set Appropriate TTL",
            description="Cache expiration based on data volatility",
            code_reference="Static data: 1 hour, Dynamic: 5 minutes",
            benefit="Balance freshness and performance",
        ),
        BestPractice(
            title="Cache-Aside Pattern",
            description="Check cache first, then DB on miss",
            code_reference="get(key) || (await fetch() && set(key))",
            benefit="Lazy loading, only cache what's needed",
        ),
        BestPractice(
            title="Implement Cache Invalidation",
            description="Clear cache on data updates",
            code_reference="On PUT/DELETE, invalidate related keys",
            benefit="Prevent stale data",
        ),
        BestPractice(
            title="Use Namespaced Keys",
            description="Prefix keys by resource type",
            code_reference="'user:123', 'post:456'",
            benefit="Organization, bulk invalidation",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Cache-Aside Pattern",
            description="Check cache, fallback to DB",
            code='''const user = await cache.get('user:123') ||
  await db.user.findUnique({ where: { id: '123' } })''',
        ),
        UsageExample(
            name="Cache with TTL",
            description="Set cache with expiration",
            code='''await cache.set('user:123', user, { ttl: 3600 })  # 1 hour''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Caching everything forever",
            why="Stale data, memory bloat",
            good="Selective caching with appropriate TTL",
        ),
        AntiPattern(
            bad="No cache invalidation",
            why="Users see outdated data",
            good="Invalidate on updates/deletes",
        ),
        AntiPattern(
            bad="Caching uncacheable data",
            why="Security risks (auth tokens, sensitive data)",
            good="Only cache public or user-specific non-sensitive data",
        ),
    ]

    file_structure: dict = {
        "backend/lib/cache.ts": "Cache service (Node.js)",
        "backend/lib/cache.py": "Cache service (Python)",
    }

    cache_service_ts: str = r'''// backend/lib/cache.ts
import { createClient, RedisClientType } from 'redis'

interface CacheOptions {
  ttl?: number // Time to live in seconds
}

class CacheService {
  private client: RedisClientType
  private connected: boolean = false

  constructor() {
    this.client = createClient({
      url: process.env.REDIS_URL || 'redis://localhost:6379',
    })

    this.client.on('error', (err) => {
      console.error('Redis error:', err)
    })

    this.client.on('connect', () => {
      this.connected = true
      console.log('Redis connected')
    })
  }

  async connect(): Promise<void> {
    if (!this.connected) {
      await this.client.connect()
    }
  }

  async disconnect(): Promise<void> {
    await this.client.disconnect()
    this.connected = false
  }

  async get<T>(key: string): Promise<T | null> {
    try {
      const value = await this.client.get(key)
      return value ? JSON.parse(value) : null
    } catch (error) {
      console.error(`Cache get error for key ${key}:`, error)
      return null
    }
  }

  async set<T>(key: string, value: T, options?: CacheOptions): Promise<void> {
    try {
      const serialized = JSON.stringify(value)

      if (options?.ttl) {
        await this.client.setEx(key, options.ttl, serialized)
      } else {
        await this.client.set(key, serialized)
      }
    } catch (error) {
      console.error(`Cache set error for key ${key}:`, error)
    }
  }

  async delete(key: string): Promise<void> {
    try {
      await this.client.del(key)
    } catch (error) {
      console.error(`Cache delete error for key ${key}:`, error)
    }
  }

  async deletePattern(pattern: string): Promise<void> {
    try {
      const keys = await this.client.keys(pattern)
      if (keys.length > 0) {
        await this.client.del(keys)
      }
    } catch (error) {
      console.error(`Cache delete pattern error for ${pattern}:`, error)
    }
  }

  async exists(key: string): Promise<boolean> {
    try {
      const result = await this.client.exists(key)
      return result === 1
    } catch (error) {
      console.error(`Cache exists error for key ${key}:`, error)
      return false
    }
  }

  async clear(): Promise<void> {
    try {
      await this.client.flushAll()
    } catch (error) {
      console.error('Cache clear error:', error)
    }
  }

  // Cache-aside pattern helper
  async getOrSet<T>(
    key: string,
    fetcher: () => Promise<T>,
    options?: CacheOptions
  ): Promise<T> {
    // Try to get from cache
    const cached = await this.get<T>(key)
    if (cached !== null) {
      return cached
    }

    // Cache miss - fetch data
    const data = await fetcher()

    // Store in cache
    await this.set(key, data, options)

    return data
  }
}

export const cache = new CacheService()

// In-memory cache for development
class MemoryCache {
  private store: Map<string, { value: any; expires?: number }> = new Map()

  get<T>(key: string): T | null {
    const item = this.store.get(key)

    if (!item) return null

    // Check expiration
    if (item.expires && Date.now() > item.expires) {
      this.store.delete(key)
      return null
    }

    return item.value
  }

  set<T>(key: string, value: T, options?: CacheOptions): void {
    const expires = options?.ttl ? Date.now() + options.ttl * 1000 : undefined
    this.store.set(key, { value, expires })
  }

  delete(key: string): void {
    this.store.delete(key)
  }

  clear(): void {
    this.store.clear()
  }

  async getOrSet<T>(
    key: string,
    fetcher: () => Promise<T>,
    options?: CacheOptions
  ): Promise<T> {
    const cached = this.get<T>(key)
    if (cached !== null) {
      return cached
    }

    const data = await fetcher()
    this.set(key, data, options)
    return data
  }
}

export const memoryCache = new MemoryCache()
'''

    cache_service_py: str = r'''# backend/lib/cache.py
from typing import Optional, Any, Callable
import redis.asyncio as redis
import json
import os
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class CacheService:
    """Redis cache service."""

    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.client: Optional[redis.Redis] = None

    async def connect(self):
        """Connect to Redis."""
        try:
            self.client = await redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            await self.client.ping()
            logger.info("Redis connected")
        except Exception as e:
            logger.error(f"Redis connection error: {e}")
            raise

    async def disconnect(self):
        """Disconnect from Redis."""
        if self.client:
            await self.client.close()
            logger.info("Redis disconnected")

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            value = await self.client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> None:
        """Set value in cache with optional TTL (seconds)."""
        try:
            serialized = json.dumps(value)

            if ttl:
                await self.client.setex(key, ttl, serialized)
            else:
                await self.client.set(key, serialized)
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")

    async def delete(self, key: str) -> None:
        """Delete key from cache."""
        try:
            await self.client.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")

    async def delete_pattern(self, pattern: str) -> None:
        """Delete all keys matching pattern."""
        try:
            keys = await self.client.keys(pattern)
            if keys:
                await self.client.delete(*keys)
        except Exception as e:
            logger.error(f"Cache delete pattern error for {pattern}: {e}")

    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        try:
            return await self.client.exists(key) == 1
        except Exception as e:
            logger.error(f"Cache exists error for key {key}: {e}")
            return False

    async def clear(self) -> None:
        """Clear all cache."""
        try:
            await self.client.flushall()
        except Exception as e:
            logger.error(f"Cache clear error: {e}")

    async def get_or_set(
        self,
        key: str,
        fetcher: Callable,
        ttl: Optional[int] = None
    ) -> Any:
        """Cache-aside pattern: get from cache or fetch and set."""
        # Try cache first
        cached = await self.get(key)
        if cached is not None:
            return cached

        # Cache miss - fetch data
        data = await fetcher()

        # Store in cache
        await self.set(key, data, ttl)

        return data

# Singleton instance
cache = CacheService()

# In-memory cache for development/testing
class MemoryCache:
    """Simple in-memory cache."""

    def __init__(self):
        self.store: dict = {}

    async def get(self, key: str) -> Optional[Any]:
        """Get value from memory cache."""
        item = self.store.get(key)
        if not item:
            return None

        # Check expiration
        if "expires" in item and item["expires"] < 0:
            del self.store[key]
            return None

        return item["value"]

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in memory cache."""
        import time
        expires = time.time() + ttl if ttl else None
        self.store[key] = {"value": value, "expires": expires}

    async def delete(self, key: str) -> None:
        """Delete key from memory cache."""
        self.store.pop(key, None)

    async def clear(self) -> None:
        """Clear all memory cache."""
        self.store.clear()

    async def get_or_set(
        self,
        key: str,
        fetcher: Callable,
        ttl: Optional[int] = None
    ) -> Any:
        """Cache-aside pattern for memory cache."""
        cached = await self.get(key)
        if cached is not None:
            return cached

        data = await fetcher()
        await self.set(key, data, ttl)
        return data

memory_cache = MemoryCache()
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "backend/lib/cache.ts": self.cache_service_ts,
            "backend/lib/cache.py": self.cache_service_py,
        }
