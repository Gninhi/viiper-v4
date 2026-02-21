"""
Collective Knowledge Base for VIIPER.

Stores and retrieves shared knowledge across agent executions.
Enables learning from patterns and improving over time.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
import json
import hashlib


class KnowledgeType(str, Enum):
    """Types of knowledge stored in CKB."""
    PATTERN = "pattern"
    LEARNING = "learning"
    TEMPLATE = "template"
    BEST_PRACTICE = "best_practice"
    ANTI_PATTERN = "anti_pattern"
    SOLUTION = "solution"
    WORKFLOW = "workflow"


class KnowledgeEntry(BaseModel):
    """A single knowledge entry in the CKB."""
    id: str
    type: KnowledgeType
    title: str
    content: Dict[str, Any]
    tags: List[str] = Field(default_factory=list)
    source_agent: str = ""
    project_id: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    confidence: float = Field(default=0.5, ge=0, le=1)
    usage_count: int = 0
    success_rate: float = Field(default=0.5, ge=0, le=1)
    
    def update_usage(self, success: bool) -> None:
        """Update usage statistics."""
        self.usage_count += 1
        # Rolling average of success rate
        self.success_rate = (
            (self.success_rate * (self.usage_count - 1) + (1 if success else 0))
            / self.usage_count
        )
        self.updated_at = datetime.now()


class Pattern(BaseModel):
    """A reusable pattern discovered from agent executions."""
    name: str
    description: str
    triggers: List[str] = Field(default_factory=list)  # Conditions that trigger this pattern
    actions: List[Dict[str, Any]] = Field(default_factory=list)  # Actions to take
    expected_outcome: str = ""
    confidence: float = 0.5
    examples: List[Dict[str, Any]] = Field(default_factory=list)


class Learning(BaseModel):
    """A learning from agent execution."""
    context: Dict[str, Any]
    observation: str
    insight: str
    adjustment: str
    confidence: float = 0.5


class CollectiveKnowledgeBase:
    """
    Collective Knowledge Base for storing and retrieving shared knowledge.
    
    Features:
    - Pattern storage and retrieval
    - Learning accumulation
    - Semantic search (with vector DB integration)
    - Knowledge contribution from agents
    """
    
    def __init__(self, storage_backend: str = "memory"):
        """
        Initialize CKB.
        
        Args:
            storage_backend: Storage type ("memory", "file", "vector")
        """
        self.storage_backend = storage_backend
        self.knowledge: Dict[str, KnowledgeEntry] = {}
        self.patterns: Dict[str, Pattern] = {}
        self.learnings: List[Learning] = []
        self.index: Dict[str, List[str]] = {}  # Tag-based index
        
    def contribute(
        self,
        type: KnowledgeType,
        title: str,
        content: Dict[str, Any],
        tags: List[str] = None,
        source_agent: str = "",
        project_id: str = "",
        confidence: float = 0.5,
    ) -> KnowledgeEntry:
        """
        Contribute knowledge to the CKB.
        
        Args:
            type: Type of knowledge
            title: Title/description
            content: Knowledge content
            tags: Tags for indexing
            source_agent: Agent that contributed
            project_id: Related project
            confidence: Confidence level
            
        Returns:
            Created knowledge entry
        """
        # Generate ID
        content_hash = hashlib.md5(
            json.dumps(content, sort_keys=True).encode()
        ).hexdigest()[:8]
        entry_id = f"{type.value}_{content_hash}"
        
        entry = KnowledgeEntry(
            id=entry_id,
            type=type,
            title=title,
            content=content,
            tags=tags or [],
            source_agent=source_agent,
            project_id=project_id,
            confidence=confidence,
        )
        
        # Store
        self.knowledge[entry_id] = entry
        
        # Index by tags
        for tag in (tags or []):
            if tag not in self.index:
                self.index[tag] = []
            self.index[tag].append(entry_id)
        
        # Store pattern if applicable
        if type == KnowledgeType.PATTERN:
            pattern = Pattern(
                name=title,
                description=content.get("description", ""),
                triggers=content.get("triggers", []),
                actions=content.get("actions", []),
                expected_outcome=content.get("expected_outcome", ""),
                confidence=confidence,
            )
            self.patterns[entry_id] = pattern
        
        # Store learning if applicable
        if type == KnowledgeType.LEARNING:
            learning = Learning(
                context=content.get("context", {}),
                observation=content.get("observation", ""),
                insight=content.get("insight", ""),
                adjustment=content.get("adjustment", ""),
                confidence=confidence,
            )
            self.learnings.append(learning)
        
        return entry
    
    def search(
        self,
        query: str,
        tags: List[str] = None,
        type: KnowledgeType = None,
        limit: int = 10,
    ) -> List[KnowledgeEntry]:
        """
        Search the CKB.
        
        Args:
            query: Search query
            tags: Filter by tags
            type: Filter by type
            limit: Maximum results
            
        Returns:
            Matching knowledge entries
        """
        results = []
        
        # Get candidates from tag index
        candidate_ids = set()
        if tags:
            for tag in tags:
                candidate_ids.update(self.index.get(tag, []))
        else:
            candidate_ids = set(self.knowledge.keys())
        
        # Filter and rank
        for entry_id in candidate_ids:
            entry = self.knowledge.get(entry_id)
            if not entry:
                continue
            
            # Filter by type
            if type and entry.type != type:
                continue
            
            # Simple text matching
            query_lower = query.lower()
            if (
                query_lower in entry.title.lower()
                or any(query_lower in tag.lower() for tag in entry.tags)
                or query_lower in str(entry.content).lower()
            ):
                results.append(entry)
        
        # Sort by confidence and usage
        results.sort(key=lambda e: (e.confidence * e.success_rate, e.usage_count), reverse=True)
        
        return results[:limit]
    
    def get_patterns_for_context(self, context: Dict[str, Any]) -> List[Pattern]:
        """
        Get patterns applicable to a context.
        
        Args:
            context: Current execution context
            
        Returns:
            Applicable patterns
        """
        applicable = []
        
        for pattern in self.patterns.values():
            # Check if any trigger matches context
            context_str = json.dumps(context).lower()
            if any(trigger.lower() in context_str for trigger in pattern.triggers):
                applicable.append(pattern)
        
        # Sort by confidence
        applicable.sort(key=lambda p: p.confidence, reverse=True)
        
        return applicable
    
    def get_learnings_for_agent(self, agent_name: str) -> List[Learning]:
        """
        Get learnings relevant to an agent.
        
        Args:
            agent_name: Agent name
            
        Returns:
            Relevant learnings
        """
        # Filter learnings by agent context
        relevant = []
        for learning in self.learnings:
            if agent_name.lower() in str(learning.context).lower():
                relevant.append(learning)
        
        return relevant
    
    def record_usage(self, entry_id: str, success: bool) -> None:
        """
        Record usage of a knowledge entry.
        
        Args:
            entry_id: Entry ID
            success: Whether usage was successful
        """
        entry = self.knowledge.get(entry_id)
        if entry:
            entry.update_usage(success)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get CKB statistics."""
        return {
            "total_entries": len(self.knowledge),
            "patterns": len(self.patterns),
            "learnings": len(self.learnings),
            "tags": len(self.index),
            "by_type": {
                t.value: len([e for e in self.knowledge.values() if e.type == t])
                for t in KnowledgeType
            },
            "avg_confidence": sum(e.confidence for e in self.knowledge.values()) / max(len(self.knowledge), 1),
            "avg_success_rate": sum(e.success_rate for e in self.knowledge.values()) / max(len(self.knowledge), 1),
        }
    
    def export_knowledge(self) -> Dict[str, Any]:
        """Export all knowledge for backup/transfer."""
        return {
            "knowledge": {k: v.model_dump() for k, v in self.knowledge.items()},
            "patterns": {k: v.model_dump() for k, v in self.patterns.items()},
            "learnings": [l.model_dump() for l in self.learnings],
            "index": self.index,
        }
    
    def import_knowledge(self, data: Dict[str, Any]) -> None:
        """Import knowledge from backup/transfer."""
        # Import knowledge entries
        for entry_id, entry_data in data.get("knowledge", {}).items():
            self.knowledge[entry_id] = KnowledgeEntry(**entry_data)
        
        # Import patterns
        for pattern_id, pattern_data in data.get("patterns", {}).items():
            self.patterns[pattern_id] = Pattern(**pattern_data)
        
        # Import learnings
        for learning_data in data.get("learnings", []):
            self.learnings.append(Learning(**learning_data))
        
        # Import index
        self.index = data.get("index", {})


# Global CKB instance
_ckb_instance: Optional[CollectiveKnowledgeBase] = None


def get_ckb() -> CollectiveKnowledgeBase:
    """Get the global CKB instance."""
    global _ckb_instance
    if _ckb_instance is None:
        _ckb_instance = CollectiveKnowledgeBase()
    return _ckb_instance


def contribute_knowledge(
    type: KnowledgeType,
    title: str,
    content: Dict[str, Any],
    **kwargs,
) -> KnowledgeEntry:
    """Contribute knowledge to the global CKB."""
    return get_ckb().contribute(type, title, content, **kwargs)


def search_knowledge(query: str, **kwargs) -> List[KnowledgeEntry]:
    """Search the global CKB."""
    return get_ckb().search(query, **kwargs)