"""Unit tests for core classes."""

import pytest
from datetime import datetime, timedelta

from viiper.core.phase import Phase
from viiper.core.variant import Variant
from viiper.core.project import Project
from viiper.core.health import HealthScore, DimensionScore, HealthDimension


class TestPhase:
    """Tests for Phase enum."""
    
    def test_phase_values(self):
        """Test all phase values exist."""
        assert Phase.VALIDATION.value == "validation"
        assert Phase.IDEATION.value == "ideation"
        assert Phase.PRODUCTION.value == "production"
        assert Phase.EXECUTION.value == "execution"
        assert Phase.RENTABILISATION.value == "rentabilisation"
        assert Phase.ITERATION.value == "iteration"
    
    def test_phase_short_codes(self):
        """Test phase short codes."""
        assert Phase.VALIDATION.short_code == "V"
        assert Phase.IDEATION.short_code == "I"
        assert Phase.PRODUCTION.short_code == "P"
        assert Phase.EXECUTION.short_code == "E"
        assert Phase.RENTABILISATION.short_code == "R"
        assert Phase.ITERATION.short_code == "I²"
    
    def test_phase_navigation(self):
        """Test phase navigation."""
        assert Phase.VALIDATION.next_phase() == Phase.IDEATION
        assert Phase.IDEATION.next_phase() == Phase.PRODUCTION
        assert Phase.ITERATION.next_phase() is None
        
        assert Phase.IDEATION.previous_phase() == Phase.VALIDATION
        assert Phase.VALIDATION.previous_phase() is None


class TestVariant:
    """Tests for Variant enum."""
    
    def test_variant_values(self):
        """Test all variant values exist."""
        assert Variant.LANDING.value == "landing"
        assert Variant.SAAS.value == "saas"
        assert Variant.MOBILE.value == "mobile"
    
    def test_variant_requirements(self):
        """Test variant requirements."""
        assert Variant.SAAS.requires_authentication is True
        assert Variant.LANDING.requires_authentication is False
        
        assert Variant.SAAS.requires_payments is True
        assert Variant.WEB.requires_payments is False
    
    def test_variant_metrics(self):
        """Test variant has primary metrics."""
        metrics = Variant.SAAS.primary_metrics
        assert "MRR" in metrics
        assert "Churn" in metrics
        assert "LTV/CAC" in metrics


class TestHealthScore:
    """Tests for HealthScore."""
    
    def test_dimension_score_creation(self):
        """Test creating dimension score."""
        score = DimensionScore(
            dimension=HealthDimension.PERFORMANCE,
            score=8.5,
            metrics={"code_quality": 9.0, "test_coverage": 8.0}
        )
        
        assert score.score == 8.5
        assert score.status in ["✅ Excellent", "✅ Good"]
    
    def test_health_score_overall(self):
        """Test overall health score calculation."""
        health = HealthScore(
            performance=DimensionScore(dimension=HealthDimension.PERFORMANCE, score=8.0),
            acquisition=DimensionScore(dimension=HealthDimension.ACQUISITION, score=7.0),
            engagement=DimensionScore(dimension=HealthDimension.ENGAGEMENT, score=8.0),
            revenue=DimensionScore(dimension=HealthDimension.REVENUE, score=6.0)
        )
        
        # With equal weights (0.25 each): (8 + 7 + 8 + 6) / 4 = 7.25
        assert 7.2 <= health.overall <= 7.3
    
    def test_health_alerts(self):
        """Test health alerts for critical scores."""
        health = HealthScore(
            performance=DimensionScore(dimension=HealthDimension.PERFORMANCE, score=2.0),
            acquisition=DimensionScore(dimension=HealthDimension.ACQUISITION, score=7.0),
            engagement=DimensionScore(dimension=HealthDimension.ENGAGEMENT, score=8.0),
            revenue=DimensionScore(dimension=HealthDimension.REVENUE, score=6.0)
        )
        
        alerts = health.get_alerts()
        assert len(alerts) > 0
        assert any("Performance" in alert for alert in alerts)


class TestProject:
    """Tests for Project model."""
    
    def test_project_creation(self):
        """Test creating a project."""
        project = Project(
            name="Test SaaS",
            variant=Variant.SAAS,
            budget=10000,
            timeline_weeks=12
        )
        
        assert project.name == "Test SaaS"
        assert project.variant == Variant.SAAS
        assert project.phase == Phase.VALIDATION  # Default
        assert project.budget == 10000
    
    def test_phase_transition(self):
        """Test phase transitions."""
        project = Project(
            name="Test Project",
            variant=Variant.SAAS,
            budget=10000,
            timeline_weeks=12,
            phase=Phase.VALIDATION
        )
        
        # Can transition to next phase
        success = project.transition_to_phase(Phase.IDEATION)
        assert success is True
        assert project.phase == Phase.IDEATION
        
        # Cannot skip phases
        success = project.transition_to_phase(Phase.EXECUTION)
        assert success is False
    
    def test_timeline_progress(self):
        """Test timeline progress calculation."""
        project = Project(
            name="Test Project",
            variant=Variant.SAAS,
            budget=10000,
            timeline_weeks=10,
            started_at=datetime.now() - timedelta(weeks=5)
        )
        
        progress = project.get_timeline_progress()
        assert 0.4 <= progress <= 0.6  # ~50% progress
    
    def test_budget_tracking(self):
        """Test budget tracking."""
        project = Project(
            name="Test Project",
            variant=Variant.SAAS,
            budget=10000,
            timeline_weeks=12,
            budget_spent=5000
        )
        
        usage = project.get_budget_usage()
        assert usage == 0.5  # 50% spent
    
    def test_health_calculation(self):
        """Test health score calculation."""
        project = Project(
            name="Test Project",
            variant=Variant.SAAS,
            budget=10000,
            timeline_weeks=12,
            current_users=50,
            target_users=100,
            budget_spent=3000
        )
        
        health = project.calculate_health_score()
        assert health.overall >= 0.0
        assert health.overall <= 10.0
        assert health.performance is not None
