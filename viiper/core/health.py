"""
Health scoring system for VIIPER projects.

Monitors project health across multiple dimensions with
composite scoring and alerting.
"""

from typing import Dict, Optional
from pydantic import BaseModel, Field
from enum import Enum


class HealthDimension(str, Enum):
    """Health monitoring dimensions."""
    
    PERFORMANCE = "performance"  # Code quality, tests, security
    ACQUISITION = "acquisition"  # User growth, activation
    ENGAGEMENT = "engagement"    # Retention, activity
    REVENUE = "revenue"          # Monetization, unit economics
    
    @property
    def display_name(self) -> str:
        """Get display name."""
        return self.value.capitalize()


class DimensionScore(BaseModel):
    """Score for a single health dimension."""
    
    dimension: HealthDimension
    score: float = Field(ge=0.0, le=10.0, description="Score from 0-10")
    weight: float = Field(ge=0.0, le=1.0, default=0.25, description="Weight in overall score")
    metrics: Dict[str, float] = Field(default_factory=dict, description="Individual metrics")
    notes: Optional[str] = Field(default=None, description="Additional context")
    
    @property
    def status(self) -> str:
        """Get status based on score."""
        if self.score >= 8.0:
            return "✅ Excellent"
        elif self.score >= 7.0:
            return "✅ Good"
        elif self.score >= 5.0:
            return "⚠️ Fair"
        elif self.score >= 3.0:
            return "⚠️ Poor"
        else:
            return "❌ Critical"
    
    def __str__(self) -> str:
        return f"{self.dimension.display_name}: {self.score:.1f}/10 {self.status}"


class HealthScore(BaseModel):
    """
    Composite health score for a VIIPER project.
    
    Tracks health across 4 dimensions with weighted scoring.
    """
    
    performance: DimensionScore = Field(description="Performance metrics")
    acquisition: DimensionScore = Field(description="User acquisition metrics")
    engagement: DimensionScore = Field(description="Engagement metrics")
    revenue: DimensionScore = Field(description="Revenue metrics")
    
    @property
    def overall(self) -> float:
        """Calculate weighted overall health score."""
        total_weight = (
            self.performance.weight +
            self.acquisition.weight +
            self.engagement.weight +
            self.revenue.weight
        )
        
        if total_weight == 0:
            return 0.0
        
        weighted_sum = (
            self.performance.score * self.performance.weight +
            self.acquisition.score * self.acquisition.weight +
            self.engagement.score * self.engagement.weight +
            self.revenue.score * self.revenue.weight
        )
        
        return weighted_sum / total_weight
    
    @property
    def status(self) -> str:
        """Get overall status."""
        score = self.overall
        if score >= 8.0:
            return "🟢 Excellent Health"
        elif score >= 7.0:
            return "🟢 Good Health"
        elif score >= 5.0:
            return "🟡 Fair Health"
        elif score >= 3.0:
            return "🟠 Poor Health"
        else:
            return "🔴 Critical Health"
    
    @property
    def requires_intervention(self) -> bool:
        """Does the project require immediate intervention?"""
        # Critical if overall < 5 OR any dimension < 3
        if self.overall < 5.0:
            return True
        
        return any([
            self.performance.score < 3.0,
            self.acquisition.score < 3.0,
            self.engagement.score < 3.0,
            self.revenue.score < 3.0
        ])
    
    @property
    def weakest_dimension(self) -> DimensionScore:
        """Get the weakest dimension."""
        dimensions = [self.performance, self.acquisition, self.engagement, self.revenue]
        return min(dimensions, key=lambda d: d.score)
    
    @property
    def strongest_dimension(self) -> DimensionScore:
        """Get the strongest dimension."""
        dimensions = [self.performance, self.acquisition, self.engagement, self.revenue]
        return max(dimensions, key=lambda d: d.score)
    
    def get_alerts(self) -> list[str]:
        """Get list of health alerts."""
        alerts = []
        
        if self.overall < 5.0:
            alerts.append(f"🔴 CRITICAL: Overall health low ({self.overall:.1f}/10)")
        
        for dimension in [self.performance, self.acquisition, self.engagement, self.revenue]:
            if dimension.score < 3.0:
                alerts.append(
                    f"🔴 CRITICAL: {dimension.dimension.display_name} "
                    f"critically low ({dimension.score:.1f}/10)"
                )
            elif dimension.score < 5.0:
                alerts.append(
                    f"⚠️ WARNING: {dimension.dimension.display_name} "
                    f"below target ({dimension.score:.1f}/10)"
                )
        
        return alerts
    
    def to_dict(self) -> Dict[str, any]:
        """Convert to dictionary representation."""
        return {
            "overall_score": round(self.overall, 2),
            "status": self.status,
            "dimensions": {
                "performance": {
                    "score": self.performance.score,
                    "weight": self.performance.weight,
                    "status": self.performance.status,
                    "metrics": self.performance.metrics
                },
                "acquisition": {
                    "score": self.acquisition.score,
                    "weight": self.acquisition.weight,
                    "status": self.acquisition.status,
                    "metrics": self.acquisition.metrics
                },
                "engagement": {
                    "score": self.engagement.score,
                    "weight": self.engagement.weight,
                    "status": self.engagement.status,
                    "metrics": self.engagement.metrics
                },
                "revenue": {
                    "score": self.revenue.score,
                    "weight": self.revenue.weight,
                    "status": self.revenue.status,
                    "metrics": self.revenue.metrics
                }
            },
            "alerts": self.get_alerts(),
            "requires_intervention": self.requires_intervention
        }
    
    def __str__(self) -> str:
        """String representation."""
        lines = [
            f"\n{'='*50}",
            f"VIIPER Health Score: {self.overall:.1f}/10 - {self.status}",
            f"{'='*50}",
            "",
            str(self.performance),
            str(self.acquisition),
            str(self.engagement),
            str(self.revenue),
            ""
        ]
        
        alerts = self.get_alerts()
        if alerts:
            lines.append("Alerts:")
            lines.extend([f"  {alert}" for alert in alerts])
            lines.append("")
        
        lines.append(f"{'='*50}\n")
        return "\n".join(lines)
