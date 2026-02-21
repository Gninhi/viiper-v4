"""
Tests for Quality Gates system.

Ensures phase transitions are properly validated.
"""

import pytest
from datetime import datetime

from viiper.core.project import Project, ProjectMetadata
from viiper.core.phase import Phase
from viiper.core.variant import Variant
from viiper.core.health import HealthScore, DimensionScore, HealthDimension
from viiper.core.quality_gates import (
    GateStatus,
    GateCriterion,
    GateResult,
    QualityGate,
    ValidationGate,
    IdeationGate,
    ProductionGate,
    ExecutionGate,
    RentabilisationGate,
    IterationGate,
    QualityGateRegistry,
    check_transition,
    validate_transition,
    gate_registry,
)


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def minimal_project():
    """Create a minimal project for testing."""
    return Project(
        name="Test Project",
        variant=Variant.SAAS,
        phase=Phase.VALIDATION,
        budget=10000.0,
        timeline_weeks=12,
    )


@pytest.fixture
def validation_ready_project():
    """Create a project ready for validation gate."""
    return Project(
        name="Validation Ready",
        variant=Variant.SAAS,
        phase=Phase.VALIDATION,
        budget=10000.0,
        timeline_weeks=12,
        metadata=ProjectMetadata(
            notes="Clear problem definition: We need to solve X for Y users in Z market. " * 5,
            target_market="SMB",
            industry="Technology",
        ),
    )


@pytest.fixture
def ideation_ready_project():
    """Create a project ready for ideation gate."""
    return Project(
        name="Ideation Ready",
        variant=Variant.SAAS,
        phase=Phase.IDEATION,
        budget=15000.0,
        budget_spent=1000.0,
        timeline_weeks=12,
        metadata=ProjectMetadata(
            notes="Architecture: Microservices with React frontend. Security: OAuth2, JWT.",
            tech_stack={"frontend": "React", "backend": "Node.js", "database": "PostgreSQL"},
            target_market="SMB",
            tags=["architecture", "security"],
        ),
    )


@pytest.fixture
def production_ready_project():
    """Create a project ready for production gate."""
    health = HealthScore(
        performance=DimensionScore(
            dimension=HealthDimension.PERFORMANCE, score=8.5, metrics={"test_coverage": 0.85}
        ),
        acquisition=DimensionScore(dimension=HealthDimension.ACQUISITION, score=7.0, metrics={}),
        engagement=DimensionScore(dimension=HealthDimension.ENGAGEMENT, score=6.5, metrics={}),
        revenue=DimensionScore(dimension=HealthDimension.REVENUE, score=5.0, metrics={}),
    )

    return Project(
        name="Production Ready",
        variant=Variant.SAAS,
        phase=Phase.PRODUCTION,
        budget=15000.0,
        budget_spent=8000.0,
        timeline_weeks=12,
        current_users=50,
        metadata=ProjectMetadata(
            notes="Architecture complete. Security scan passed. " * 10,
            tags=["features", "security", "tested"],
            tech_stack={"frontend": "React"},
        ),
        health_score=health,
    )


@pytest.fixture
def execution_ready_project():
    """Create a project ready for execution gate."""
    return Project(
        name="Execution Ready",
        variant=Variant.SAAS,
        phase=Phase.EXECUTION,
        budget=15000.0,
        budget_spent=12000.0,
        timeline_weeks=12,
        current_users=150,
        metadata=ProjectMetadata(
            notes="Launched to public. Marketing channels: SEO, Ads, Content.",
            tags=["launched"],
        ),
    )


@pytest.fixture
def rentabilisation_ready_project():
    """Create a project ready for rentabilisation gate."""
    health = HealthScore(
        performance=DimensionScore(dimension=HealthDimension.PERFORMANCE, score=8.0, metrics={}),
        acquisition=DimensionScore(
            dimension=HealthDimension.ACQUISITION, score=7.5, metrics={"cac": 50}
        ),
        engagement=DimensionScore(
            dimension=HealthDimension.ENGAGEMENT, score=7.0, metrics={"retention": 0.6}
        ),
        revenue=DimensionScore(
            dimension=HealthDimension.REVENUE, score=6.0, metrics={"ltv": 150, "mrr": 5000}
        ),
    )

    return Project(
        name="Rentabilisation Ready",
        variant=Variant.SAAS,
        phase=Phase.RENTABILISATION,
        budget=15000.0,
        budget_spent=14000.0,
        timeline_weeks=12,
        current_users=500,
        current_revenue=5000.0,
        target_revenue=10000.0,
        health_score=health,
    )


# =============================================================================
# GATE CRITERION TESTS
# =============================================================================


class TestGateCriterion:
    """Test individual gate criteria."""

    def test_criterion_pass(self, minimal_project):
        """Test criterion that passes."""
        criterion = GateCriterion(
            name="Budget Check",
            description="Budget must be > 0",
            check_func=lambda p: p.budget > 0,
            required=True,
        )

        status, message = criterion.evaluate(minimal_project)

        assert status == GateStatus.PASSED
        assert "Passed" in message

    def test_criterion_fail(self, minimal_project):
        """Test criterion that fails."""
        criterion = GateCriterion(
            name="Negative Check",
            description="Budget must be negative",
            check_func=lambda p: p.budget < 0,
            required=True,
        )

        status, message = criterion.evaluate(minimal_project)

        assert status == GateStatus.FAILED
        assert "Failed" in message

    def test_criterion_with_custom_message(self, minimal_project):
        """Test criterion returning custom message."""
        criterion = GateCriterion(
            name="Custom Message",
            description="Returns custom message",
            check_func=lambda p: (True, "Custom success message"),
            required=True,
        )

        status, message = criterion.evaluate(minimal_project)

        assert status == GateStatus.PASSED
        assert message == "Custom success message"

    def test_criterion_error_handling(self, minimal_project):
        """Test criterion error handling."""
        criterion = GateCriterion(
            name="Error Test",
            description="Raises exception",
            check_func=lambda p: 1 / 0,  # Division by zero
            required=True,
        )

        status, message = criterion.evaluate(minimal_project)

        assert status == GateStatus.FAILED
        assert "Error" in message


# =============================================================================
# VALIDATION GATE TESTS
# =============================================================================


class TestValidationGate:
    """Test Validation → Ideation gate."""

    def test_validation_gate_pass(self, validation_ready_project):
        """Test gate passes with valid project."""
        gate = ValidationGate(Phase.VALIDATION, Phase.IDEATION)
        result = gate.evaluate(validation_ready_project)

        assert result.status == GateStatus.PASSED
        assert result.can_transition is True
        assert result.score >= 7.0
        assert len(result.blocking_issues) == 0

    def test_validation_gate_fail_no_notes(self, minimal_project):
        """Test gate fails without proper documentation."""
        gate = ValidationGate(Phase.VALIDATION, Phase.IDEATION)
        result = gate.evaluate(minimal_project)

        assert result.status == GateStatus.FAILED
        assert result.can_transition is False
        assert len(result.blocking_issues) > 0

    def test_validation_gate_checks_all_criteria(self, validation_ready_project):
        """Test that all criteria are evaluated."""
        gate = ValidationGate(Phase.VALIDATION, Phase.IDEATION)
        result = gate.evaluate(validation_ready_project)

        assert len(result.criteria_results) == 4  # Problem, Market, Budget, Timeline

        criteria_names = [r["criterion"] for r in result.criteria_results]
        assert "Problem Definition" in criteria_names
        assert "Target Market" in criteria_names
        assert "Budget Allocation" in criteria_names
        assert "Timeline Planning" in criteria_names


# =============================================================================
# IDEATION GATE TESTS
# =============================================================================


class TestIdeationGate:
    """Test Ideation → Production gate."""

    def test_ideation_gate_pass(self, ideation_ready_project):
        """Test gate passes with valid project."""
        gate = IdeationGate(Phase.IDEATION, Phase.PRODUCTION)
        result = gate.evaluate(ideation_ready_project)

        assert result.status == GateStatus.PASSED
        assert result.can_transition is True

    def test_ideation_gate_fail_no_architecture(self, minimal_project):
        """Test gate fails without architecture."""
        minimal_project.phase = Phase.IDEATION
        gate = IdeationGate(Phase.IDEATION, Phase.PRODUCTION)
        result = gate.evaluate(minimal_project)

        assert result.status == GateStatus.FAILED
        assert result.can_transition is False


# =============================================================================
# PRODUCTION GATE TESTS
# =============================================================================


class TestProductionGate:
    """Test Production → Execution gate."""

    def test_production_gate_pass(self, production_ready_project):
        """Test gate passes with valid project."""
        gate = ProductionGate(Phase.PRODUCTION, Phase.EXECUTION)
        result = gate.evaluate(production_ready_project)

        # Should pass or at least not fail (might be warning)
        assert result.status in [GateStatus.PASSED, GateStatus.WARNING]

    def test_production_gate_higher_threshold(self):
        """Test that production gate has higher minimum score."""
        gate = ProductionGate(Phase.PRODUCTION, Phase.EXECUTION)

        assert gate.minimum_score == 8.0

    def test_production_gate_fail_no_features(self, minimal_project):
        """Test gate fails without features."""
        minimal_project.phase = Phase.PRODUCTION
        gate = ProductionGate(Phase.PRODUCTION, Phase.EXECUTION)
        result = gate.evaluate(minimal_project)

        assert result.status == GateStatus.FAILED
        assert "Core Features" in str(result.blocking_issues)


# =============================================================================
# EXECUTION GATE TESTS
# =============================================================================


class TestExecutionGate:
    """Test Execution → Rentabilisation gate."""

    def test_execution_gate_pass(self, execution_ready_project):
        """Test gate passes with valid project."""
        gate = ExecutionGate(Phase.EXECUTION, Phase.RENTABILISATION)
        result = gate.evaluate(execution_ready_project)

        assert result.status == GateStatus.PASSED
        assert result.can_transition is True

    def test_execution_gate_fail_no_users(self, minimal_project):
        """Test gate fails without user base."""
        minimal_project.phase = Phase.EXECUTION
        gate = ExecutionGate(Phase.EXECUTION, Phase.RENTABILISATION)
        result = gate.evaluate(minimal_project)

        assert result.status == GateStatus.FAILED
        assert "User Base" in str(result.blocking_issues)


# =============================================================================
# RENTABILISATION GATE TESTS
# =============================================================================


class TestRentabilisationGate:
    """Test Rentabilisation → Iteration gate."""

    def test_rentabilisation_gate_pass(self, rentabilisation_ready_project):
        """Test gate passes with valid project."""
        gate = RentabilisationGate(Phase.RENTABILISATION, Phase.ITERATION)
        result = gate.evaluate(rentabilisation_ready_project)

        assert result.status == GateStatus.PASSED
        assert result.can_transition is True

    def test_rentabilisation_gate_fail_no_revenue(self, minimal_project):
        """Test gate fails without revenue."""
        minimal_project.phase = Phase.RENTABILISATION
        gate = RentabilisationGate(Phase.RENTABILISATION, Phase.ITERATION)
        result = gate.evaluate(minimal_project)

        assert result.status == GateStatus.FAILED
        assert "Revenue Stream" in str(result.blocking_issues)


# =============================================================================
# ITERATION GATE TESTS
# =============================================================================


class TestIterationGate:
    """Test Iteration gate (continuous)."""

    def test_iteration_gate_lower_threshold(self):
        """Test that iteration gate has lower threshold."""
        gate = IterationGate(Phase.ITERATION, Phase.ITERATION)

        assert gate.minimum_score == 5.0

    def test_iteration_gate_passes_with_any_project(self, minimal_project):
        """Test iteration gate is permissive."""
        minimal_project.phase = Phase.ITERATION
        gate = IterationGate(Phase.ITERATION, Phase.ITERATION)
        result = gate.evaluate(minimal_project)

        # Should pass or warning (never blocking)
        assert result.status in [GateStatus.PASSED, GateStatus.WARNING]


# =============================================================================
# REGISTRY TESTS
# =============================================================================


class TestQualityGateRegistry:
    """Test gate registry."""

    def test_registry_has_default_gates(self):
        """Test that registry has all default gates."""
        registry = QualityGateRegistry()
        gates = registry.list_gates()

        assert len(gates) == 6

        gate_names = [g["name"] for g in gates]
        assert "Validation Gate" in gate_names
        assert "Ideation Gate" in gate_names
        assert "Production Gate" in gate_names
        assert "Execution Gate" in gate_names
        assert "Rentabilisation Gate" in gate_names
        assert "Iteration Gate" in gate_names

    def test_registry_can_transition_pass(self, validation_ready_project):
        """Test can_transition returns True for valid project."""
        registry = QualityGateRegistry()
        can_transition, result = registry.can_transition(validation_ready_project, Phase.IDEATION)

        assert can_transition is True
        assert result is not None
        assert result.can_transition is True

    def test_registry_can_transition_fail(self, minimal_project):
        """Test can_transition returns False for invalid project."""
        registry = QualityGateRegistry()
        can_transition, result = registry.can_transition(minimal_project, Phase.IDEATION)

        assert can_transition is False
        assert result is not None
        assert result.can_transition is False

    def test_registry_validate_transition(self, validation_ready_project):
        """Test validate_transition returns detailed result."""
        registry = QualityGateRegistry()
        result = registry.validate_transition(validation_ready_project, Phase.IDEATION)

        assert isinstance(result, GateResult)
        assert result.gate_name == "Validation Gate"
        assert result.from_phase == Phase.VALIDATION
        assert result.to_phase == Phase.IDEATION

    def test_registry_no_gate_defined(self, minimal_project):
        """Test behavior when no gate is defined for transition."""
        registry = QualityGateRegistry()

        # Try to transition from ITERATION to VALIDATION (no gate defined)
        minimal_project.phase = Phase.ITERATION
        can_transition, result = registry.can_transition(minimal_project, Phase.VALIDATION)

        # Should allow transition when no gate defined
        assert can_transition is True
        assert result is None


# =============================================================================
# CONVENIENCE FUNCTIONS TESTS
# =============================================================================


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_check_transition(self, validation_ready_project):
        """Test check_transition function."""
        can_transition, result = check_transition(validation_ready_project, Phase.IDEATION)

        assert can_transition is True
        assert result is not None

    def test_validate_transition(self, validation_ready_project):
        """Test validate_transition function."""
        result = validate_transition(validation_ready_project, Phase.IDEATION)

        assert isinstance(result, GateResult)
        assert result.status == GateStatus.PASSED

    def test_global_registry(self):
        """Test global registry instance."""
        from viiper.core.quality_gates import gate_registry

        assert isinstance(gate_registry, QualityGateRegistry)
        assert len(gate_registry.list_gates()) == 6


# =============================================================================
# GATE RESULT TESTS
# =============================================================================


class TestGateResult:
    """Test GateResult dataclass."""

    def test_gate_result_to_dict(self):
        """Test conversion to dictionary."""
        result = GateResult(
            gate_name="Test Gate",
            from_phase=Phase.VALIDATION,
            to_phase=Phase.IDEATION,
            status=GateStatus.PASSED,
            score=8.5,
        )

        data = result.to_dict()

        assert data["gate_name"] == "Test Gate"
        assert data["from_phase"] == "validation"
        assert data["to_phase"] == "ideation"
        assert data["status"] == "passed"
        assert data["score"] == 8.5
        assert data["can_transition"] is True

    def test_gate_result_can_transition_property(self):
        """Test can_transition property."""
        passed_result = GateResult(
            gate_name="Pass",
            from_phase=Phase.VALIDATION,
            to_phase=Phase.IDEATION,
            status=GateStatus.PASSED,
            score=8.0,
        )

        failed_result = GateResult(
            gate_name="Fail",
            from_phase=Phase.VALIDATION,
            to_phase=Phase.IDEATION,
            status=GateStatus.FAILED,
            score=3.0,
        )

        assert passed_result.can_transition is True
        assert failed_result.can_transition is False

    def test_gate_result_with_criteria(self):
        """Test result with criteria results."""
        result = GateResult(
            gate_name="Test",
            from_phase=Phase.VALIDATION,
            to_phase=Phase.IDEATION,
            status=GateStatus.PASSED,
            score=8.0,
            criteria_results=[{"criterion": "Test", "status": "passed"}],
            recommendations=["Rec 1"],
            blocking_issues=[],
        )

        assert len(result.criteria_results) == 1
        assert len(result.recommendations) == 1


# =============================================================================
# END-TO-END TRANSITION TESTS
# =============================================================================


class TestEndToEndTransitions:
    """Test complete phase transitions through all gates."""

    def test_full_viiper_flow_success(self):
        """Test successful progression through all VIIPER phases."""
        # Create project at each phase and verify transitions

        # Phase 1: Validation
        project = Project(
            name="VIIPER Test",
            variant=Variant.SAAS,
            phase=Phase.VALIDATION,
            budget=10000.0,
            timeline_weeks=12,
            metadata=ProjectMetadata(
                notes="Clear problem definition for testing purposes. " * 10,
                target_market="SMB",
            ),
        )

        # V → I
        can_transition, _ = check_transition(project, Phase.IDEATION)
        assert can_transition is True
        project.phase = Phase.IDEATION

        # Add ideation artifacts
        project.metadata.tech_stack = {"frontend": "React"}
        project.metadata.notes = (
            project.metadata.notes or ""
        ) + " Architecture: Microservices. Security: OAuth2."

        # I → P
        can_transition, _ = check_transition(project, Phase.PRODUCTION)
        assert can_transition is True
        project.phase = Phase.PRODUCTION

        # Add production artifacts
        project.current_users = 50
        project.metadata.tags = ["features", "security"]
        project.health_score = HealthScore(
            performance=DimensionScore(
                dimension=HealthDimension.PERFORMANCE, score=8.0, metrics={}
            ),
            acquisition=DimensionScore(
                dimension=HealthDimension.ACQUISITION, score=7.0, metrics={}
            ),
            engagement=DimensionScore(dimension=HealthDimension.ENGAGEMENT, score=6.0, metrics={}),
            revenue=DimensionScore(dimension=HealthDimension.REVENUE, score=5.0, metrics={}),
        )

        # P → E
        can_transition, _ = check_transition(project, Phase.EXECUTION)
        assert can_transition is True
        project.phase = Phase.EXECUTION

        # Add execution artifacts (for E → R transition)
        project.current_users = 150
        project.metadata.tags = ["features", "security", "launched"]
        project.metadata.notes += (
            " Marketing channels: SEO, Ads, Content. User feedback collection via surveys."
        )

        # E → R
        can_transition, _ = check_transition(project, Phase.RENTABILISATION)
        assert can_transition is True
        project.phase = Phase.RENTABILISATION

        # Add rentabilisation artifacts
        project.current_revenue = 5000.0

        # R → I²
        can_transition, _ = check_transition(project, Phase.ITERATION)
        assert can_transition is True
        project.phase = Phase.ITERATION

        # Verify final phase
        assert project.phase == Phase.ITERATION
