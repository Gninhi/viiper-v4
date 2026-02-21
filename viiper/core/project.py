"""
Project model for VIIPER framework.

Represents a complete project with all metadata, state management,
and health monitoring.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from uuid import uuid4

from viiper.core.phase import Phase
from viiper.core.variant import Variant
from viiper.core.health import HealthScore, DimensionScore, HealthDimension

# Lazy import to avoid circular dependency
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from viiper.core.quality_gates import GateResult


class ProjectMetadata(BaseModel):
    """Extended metadata for a project."""

    tags: List[str] = Field(default_factory=list, description="Project tags")
    industry: Optional[str] = Field(default=None, description="Industry/vertical")
    target_market: Optional[str] = Field(default=None, description="Target market")
    tech_stack: Dict[str, str] = Field(default_factory=dict, description="Technology stack")
    notes: Optional[str] = Field(default=None, description="Additional notes")


class Project(BaseModel):
    """
    VIIPER Project model.

    Represents a complete product development project with
    phase tracking, health monitoring, and metadata.
    """

    # Identity
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique project ID")
    name: str = Field(description="Project name")
    variant: Variant = Field(description="Project variant type")

    # State
    phase: Phase = Field(default=Phase.VALIDATION, description="Current phase")
    status: str = Field(default="active", description="Project status")

    # Timeline
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update")
    started_at: Optional[datetime] = Field(default=None, description="Project start date")
    timeline_weeks: int = Field(gt=0, description="Planned timeline in weeks")

    # Budget
    budget: float = Field(gt=0, description="Budget in EUR")
    budget_spent: float = Field(default=0.0, ge=0, description="Budget spent")

    # Goals & Metrics
    target_users: Optional[int] = Field(default=None, description="Target user count")
    target_revenue: Optional[float] = Field(default=None, description="Target revenue")
    current_users: int = Field(default=0, ge=0, description="Current user count")
    current_revenue: float = Field(default=0.0, ge=0, description="Current revenue")

    # Health (optional - computed on demand if not set)
    health_score: Optional[HealthScore] = Field(default=None, description="Health metrics")

    # Metadata
    metadata: ProjectMetadata = Field(default_factory=ProjectMetadata)

    class Config:
        """Pydantic config."""

        json_encoders = {datetime: lambda v: v.isoformat()}

    def calculate_health_score(self) -> HealthScore:
        """
        Calculate current health score.

        This is a simplified version. In production, this would
        gather metrics from monitoring systems.
        """
        # Performance dimension
        performance_metrics = {
            "budget_efficiency": min(10.0, (self.budget / max(self.budget_spent, 1)) * 5),
            "timeline_progress": self.get_timeline_progress() * 10,
        }
        performance_score = sum(performance_metrics.values()) / len(performance_metrics)

        # Acquisition dimension
        acquisition_metrics = {
            "user_growth": min(10.0, (self.current_users / max(self.target_users or 1, 1)) * 10)
        }
        acquisition_score = sum(acquisition_metrics.values()) / len(acquisition_metrics)

        # Engagement dimension (simplified)
        engagement_score = 7.0  # Would be calculated from actual engagement data

        # Revenue dimension
        revenue_metrics = {
            "revenue_progress": min(
                10.0, (self.current_revenue / max(self.target_revenue or 1, 1)) * 10
            )
        }
        revenue_score = sum(revenue_metrics.values()) / len(revenue_metrics)

        # Create health score
        health = HealthScore(
            performance=DimensionScore(
                dimension=HealthDimension.PERFORMANCE,
                score=performance_score,
                metrics=performance_metrics,
            ),
            acquisition=DimensionScore(
                dimension=HealthDimension.ACQUISITION,
                score=acquisition_score,
                metrics=acquisition_metrics,
            ),
            engagement=DimensionScore(
                dimension=HealthDimension.ENGAGEMENT, score=engagement_score, metrics={}
            ),
            revenue=DimensionScore(
                dimension=HealthDimension.REVENUE, score=revenue_score, metrics=revenue_metrics
            ),
        )

        # Cache it
        self.health_score = health
        return health

    def transition_to_phase(
        self, next_phase: Phase, force: bool = False
    ) -> tuple[bool, Optional["GateResult"]]:
        """
        Transition to next phase with validation.

        Args:
            next_phase: Target phase to transition to
            force: If True, bypass quality gates (not recommended)

        Returns:
            Tuple of (success: bool, gate_result: Optional[GateResult])
        """
        # Lazy import to avoid circular dependency
        from viiper.core.quality_gates import check_transition

        # Check basic phase transition rules
        if not self._can_transition_to(next_phase):
            return False, None

        # Check quality gates
        can_transition, gate_result = check_transition(self, next_phase)

        if not can_transition and not force:
            return False, gate_result

        # Perform transition
        self.phase = next_phase
        self.updated_at = datetime.now()
        return True, gate_result

    def _can_transition_to(self, next_phase: Phase) -> bool:
        """Check if transition to next phase is allowed (basic rules only)."""
        current_index = list(Phase).index(self.phase)
        next_index = list(Phase).index(next_phase)

        # Can only move forward one phase at a time (or backwards)
        return abs(next_index - current_index) <= 1

    def validate_phase_transition(self, next_phase: Phase) -> "GateResult":
        """
        Validate transition to next phase without performing it.

        Args:
            next_phase: Target phase to validate

        Returns:
            GateResult with detailed validation information
        """
        from viiper.core.quality_gates import validate_transition

        return validate_transition(self, next_phase)

    def can_transition_to(self, next_phase: Phase) -> tuple[bool, Optional["GateResult"]]:
        """
        Check if project can transition to next phase.

        Args:
            next_phase: Target phase to check

        Returns:
            Tuple of (can_transition: bool, gate_result: Optional[GateResult])
        """
        from viiper.core.quality_gates import check_transition

        # Check basic rules first
        if not self._can_transition_to(next_phase):
            return False, None

        # Check quality gates
        return check_transition(self, next_phase)

    def get_timeline_progress(self) -> float:
        """Get timeline progress as percentage (0.0 - 1.0)."""
        if not self.started_at:
            return 0.0

        elapsed = (datetime.now() - self.started_at).days / 7  # weeks
        planned = self.timeline_weeks

        return min(1.0, elapsed / planned if planned > 0 else 0.0)

    def get_budget_usage(self) -> float:
        """Get budget usage as percentage (0.0 - 1.0)."""
        return min(1.0, self.budget_spent / self.budget if self.budget > 0 else 0.0)

    def is_on_track(self) -> bool:
        """Check if project is on track (budget and timeline)."""
        timeline_progress = self.get_timeline_progress()
        budget_usage = self.get_budget_usage()

        # On track if budget usage <= timeline progress (with 20% buffer)
        return budget_usage <= (timeline_progress * 1.2)

    def get_summary(self) -> Dict[str, Any]:
        """Get project summary."""
        health = self.health_score or self.calculate_health_score()

        return {
            "id": self.id,
            "name": self.name,
            "variant": self.variant.display_name,
            "phase": self.phase.display_name,
            "status": self.status,
            "timeline": {
                "weeks_planned": self.timeline_weeks,
                "progress": f"{self.get_timeline_progress() * 100:.1f}%",
            },
            "budget": {
                "total": f"€{self.budget:,.0f}",
                "spent": f"€{self.budget_spent:,.0f}",
                "remaining": f"€{self.budget - self.budget_spent:,.0f}",
                "usage": f"{self.get_budget_usage() * 100:.1f}%",
            },
            "metrics": {
                "users": f"{self.current_users} / {self.target_users or 0}",
                "revenue": f"€{self.current_revenue:,.0f} / €{self.target_revenue or 0:,.0f}",
            },
            "health": health.overall,
            "health_status": health.status,
            "on_track": self.is_on_track(),
        }

    def __str__(self) -> str:
        """String representation."""
        summary = self.get_summary()
        return (
            f"\n{'=' * 60}\n"
            f"Project: {self.name}\n"
            f"{'=' * 60}\n"
            f"Variant: {summary['variant']}\n"
            f"Phase: {summary['phase']} ({self.phase.short_code})\n"
            f"Status: {self.status}\n"
            f"\n"
            f"Timeline: {summary['timeline']['progress']} ({self.timeline_weeks} weeks planned)\n"
            f"Budget: {summary['budget']['usage']} (€{self.budget_spent:,.0f} / €{self.budget:,.0f})\n"
            f"On Track: {'✅ Yes' if summary['on_track'] else '⚠️ No'}\n"
            f"\n"
            f"Users: {summary['metrics']['users']}\n"
            f"Revenue: {summary['metrics']['revenue']}\n"
            f"\n"
            f"Health: {summary['health']:.1f}/10 - {summary['health_status']}\n"
            f"{'=' * 60}\n"
        )
