"""
Quality Gates for VIIPER phase transitions.

Ensures projects meet criteria before advancing to next phase.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

from viiper.core.project import Project
from viiper.core.phase import Phase


class GateStatus(str, Enum):
    """Status of a quality gate check."""

    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    NOT_APPLICABLE = "not_applicable"


@dataclass
class GateCriterion:
    """A single criterion within a quality gate."""

    name: str
    description: str
    check_func: Any  # Callable that returns bool
    required: bool = True
    weight: float = 1.0

    def evaluate(self, project: Project) -> tuple[GateStatus, str]:
        """Evaluate this criterion against a project."""
        try:
            result = self.check_func(project)
            if isinstance(result, tuple):
                passed, message = result
            else:
                passed = bool(result)
                message = "✅ Passed" if passed else "❌ Failed"

            status = GateStatus.PASSED if passed else GateStatus.FAILED
            return status, message
        except Exception as e:
            return GateStatus.FAILED, f"Error during evaluation: {str(e)}"


@dataclass
class GateResult:
    """Result of a quality gate evaluation."""

    gate_name: str
    from_phase: Phase
    to_phase: Phase
    status: GateStatus
    score: float  # 0.0 to 10.0
    criteria_results: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    blocking_issues: List[str] = field(default_factory=list)

    @property
    def can_transition(self) -> bool:
        """Check if transition is allowed."""
        return self.status == GateStatus.PASSED

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "gate_name": self.gate_name,
            "from_phase": self.from_phase.value,
            "to_phase": self.to_phase.value,
            "status": self.status.value,
            "score": self.score,
            "can_transition": self.can_transition,
            "criteria_results": self.criteria_results,
            "recommendations": self.recommendations,
            "blocking_issues": self.blocking_issues,
        }


class QualityGate(ABC):
    """Abstract base class for quality gates."""

    def __init__(self, from_phase: Phase, to_phase: Phase):
        self.from_phase = from_phase
        self.to_phase = to_phase
        self.criteria: List[GateCriterion] = []
        self._setup_criteria()

    @abstractmethod
    def _setup_criteria(self) -> None:
        """Setup criteria for this gate. Override in subclasses."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Get gate name."""
        pass

    @property
    def minimum_score(self) -> float:
        """Minimum score required to pass (0-10)."""
        return 7.0

    def evaluate(self, project: Project) -> GateResult:
        """Evaluate project against all criteria."""
        criteria_results = []
        total_weight = sum(c.weight for c in self.criteria)
        weighted_score = 0.0
        blocking_issues = []
        recommendations = []

        for criterion in self.criteria:
            status, message = criterion.evaluate(project)

            result = {
                "criterion": criterion.name,
                "description": criterion.description,
                "status": status.value,
                "message": message,
                "required": criterion.required,
                "weight": criterion.weight,
            }
            criteria_results.append(result)

            # Calculate weighted score
            if status == GateStatus.PASSED:
                weighted_score += 10.0 * criterion.weight / total_weight
            elif status == GateStatus.WARNING:
                weighted_score += 5.0 * criterion.weight / total_weight

            # Track blocking issues
            if status == GateStatus.FAILED and criterion.required:
                blocking_issues.append(f"{criterion.name}: {message}")

            # Generate recommendations
            if status != GateStatus.PASSED:
                recommendations.append(f"Improve {criterion.name}: {criterion.description}")

        # Determine overall status
        final_score = min(10.0, weighted_score)
        has_blocking = len(blocking_issues) > 0

        if has_blocking:
            status = GateStatus.FAILED
        elif final_score >= self.minimum_score:
            status = GateStatus.PASSED
        else:
            status = GateStatus.WARNING

        return GateResult(
            gate_name=self.name,
            from_phase=self.from_phase,
            to_phase=self.to_phase,
            status=status,
            score=round(final_score, 1),
            criteria_results=criteria_results,
            recommendations=recommendations,
            blocking_issues=blocking_issues,
        )


# =============================================================================
# CONCRETE GATE IMPLEMENTATIONS
# =============================================================================


class ValidationGate(QualityGate):
    """Gate for Validation → Ideation transition."""

    @property
    def name(self) -> str:
        return "Validation Gate"

    def _setup_criteria(self) -> None:
        self.criteria = [
            GateCriterion(
                name="Problem Definition",
                description="Clear problem statement defined",
                check_func=lambda p: (
                    len(p.metadata.notes or "") > 50 if hasattr(p, "metadata") else False
                ),
                required=True,
                weight=1.5,
            ),
            GateCriterion(
                name="Target Market",
                description="Target market identified and documented",
                check_func=lambda p: (
                    p.metadata.target_market is not None and len(p.metadata.target_market) > 0
                    if hasattr(p, "metadata")
                    else False
                ),
                required=True,
                weight=1.0,
            ),
            GateCriterion(
                name="Budget Allocation",
                description="Project budget defined and > 0",
                check_func=lambda p: p.budget > 0,
                required=True,
                weight=1.0,
            ),
            GateCriterion(
                name="Timeline Planning",
                description="Timeline defined in weeks",
                check_func=lambda p: p.timeline_weeks > 0,
                required=True,
                weight=1.0,
            ),
        ]


class IdeationGate(QualityGate):
    """Gate for Ideation → Production transition."""

    @property
    def name(self) -> str:
        return "Ideation Gate"

    def _setup_criteria(self) -> None:
        self.criteria = [
            GateCriterion(
                name="Architecture Document",
                description="System architecture documented",
                check_func=lambda p: (
                    "architecture" in (p.metadata.notes or "").lower()
                    if hasattr(p, "metadata")
                    else False
                ),
                required=True,
                weight=2.0,
            ),
            GateCriterion(
                name="Tech Stack Selection",
                description="Technology stack defined",
                check_func=lambda p: (
                    len(p.metadata.tech_stack or {}) > 0 if hasattr(p, "metadata") else False
                ),
                required=True,
                weight=1.5,
            ),
            GateCriterion(
                name="Security Planning",
                description="Security considerations documented",
                check_func=lambda p: (
                    "security" in (p.metadata.notes or "").lower()
                    if hasattr(p, "metadata")
                    else False
                ),
                required=True,
                weight=1.5,
            ),
            GateCriterion(
                name="Budget Review",
                description="Budget reviewed and still available",
                check_func=lambda p: p.budget > p.budget_spent,
                required=True,
                weight=1.0,
            ),
        ]


class ProductionGate(QualityGate):
    """Gate for Production → Execution transition."""

    @property
    def name(self) -> str:
        return "Production Gate"

    @property
    def minimum_score(self) -> float:
        return 8.0  # Higher threshold for production

    def _setup_criteria(self) -> None:
        self.criteria = [
            GateCriterion(
                name="Core Features",
                description="Core features implemented (simulated via metadata)",
                check_func=lambda p: (
                    "features" in (p.metadata.tags or []) if hasattr(p, "metadata") else False
                ),
                required=True,
                weight=2.0,
            ),
            GateCriterion(
                name="Testing Coverage",
                description="Tests passing (simulated via health score)",
                check_func=lambda p: (
                    (p.health_score.performance.score >= 7.0 if p.health_score else False)
                    or p.current_users > 0
                ),
                required=True,
                weight=2.0,
            ),
            GateCriterion(
                name="Security Scan",
                description="Security vulnerabilities addressed",
                check_func=lambda p: (
                    "security" in (p.metadata.tags or []) if hasattr(p, "metadata") else True
                ),
                required=True,
                weight=1.5,
            ),
            GateCriterion(
                name="Documentation",
                description="Technical documentation complete",
                check_func=lambda p: (
                    len(p.metadata.notes or "") > 200 if hasattr(p, "metadata") else False
                ),
                required=False,
                weight=1.0,
            ),
            GateCriterion(
                name="Performance",
                description="Performance benchmarks met",
                check_func=lambda p: (
                    p.health_score.performance.score >= 6.0 if p.health_score else True
                ),
                required=False,
                weight=1.0,
            ),
        ]


class ExecutionGate(QualityGate):
    """Gate for Execution → Rentabilisation transition."""

    @property
    def name(self) -> str:
        return "Execution Gate"

    def _setup_criteria(self) -> None:
        self.criteria = [
            GateCriterion(
                name="User Base",
                description="Active user base established",
                check_func=lambda p: p.current_users > 10,
                required=True,
                weight=2.0,
            ),
            GateCriterion(
                name="Launch Complete",
                description="Product publicly launched",
                check_func=lambda p: (
                    "launched" in (p.metadata.tags or [])
                    if hasattr(p, "metadata")
                    else p.current_users > 0
                ),
                required=True,
                weight=1.5,
            ),
            GateCriterion(
                name="Marketing Strategy",
                description="Marketing channels defined",
                check_func=lambda p: (
                    "marketing" in (p.metadata.notes or "").lower()
                    if hasattr(p, "metadata")
                    else False
                ),
                required=False,
                weight=1.0,
            ),
            GateCriterion(
                name="Feedback Loop",
                description="User feedback collection in place",
                check_func=lambda p: (
                    "feedback" in (p.metadata.notes or "").lower()
                    if hasattr(p, "metadata")
                    else False
                ),
                required=False,
                weight=1.0,
            ),
        ]


class RentabilisationGate(QualityGate):
    """Gate for Rentabilisation → Iteration transition."""

    @property
    def name(self) -> str:
        return "Rentabilisation Gate"

    def _setup_criteria(self) -> None:
        self.criteria = [
            GateCriterion(
                name="Revenue Stream",
                description="Revenue generation established",
                check_func=lambda p: p.current_revenue > 0,
                required=True,
                weight=2.0,
            ),
            GateCriterion(
                name="Unit Economics",
                description="CAC and LTV understood",
                check_func=lambda p: (
                    p.health_score.revenue.score >= 5.0 if p.health_score else p.current_revenue > 0
                ),
                required=False,
                weight=1.5,
            ),
            GateCriterion(
                name="Growth Metrics",
                description="Growth metrics tracked",
                check_func=lambda p: (
                    p.health_score.acquisition.score >= 5.0
                    if p.health_score
                    else p.current_users > 0
                ),
                required=False,
                weight=1.0,
            ),
            GateCriterion(
                name="Retention",
                description="User retention measured",
                check_func=lambda p: (
                    p.health_score.engagement.score >= 5.0 if p.health_score else True
                ),
                required=False,
                weight=1.0,
            ),
        ]


class IterationGate(QualityGate):
    """Gate for continuous iteration phase."""

    @property
    def name(self) -> str:
        return "Iteration Gate"

    @property
    def minimum_score(self) -> float:
        return 5.0  # Lower threshold for iteration

    def _setup_criteria(self) -> None:
        self.criteria = [
            GateCriterion(
                name="Continuous Deployment",
                description="Deployment pipeline operational",
                check_func=lambda p: True,  # Always pass for iteration
                required=False,
                weight=1.0,
            ),
            GateCriterion(
                name="Metrics Dashboard",
                description="Analytics and monitoring in place",
                check_func=lambda p: p.health_score is not None,
                required=False,
                weight=1.0,
            ),
        ]


# =============================================================================
# GATE REGISTRY
# =============================================================================


class QualityGateRegistry:
    """Registry of all quality gates."""

    def __init__(self):
        self._gates: Dict[tuple[Phase, Phase], QualityGate] = {}
        self._register_default_gates()

    def _register_default_gates(self) -> None:
        """Register default VIIPER gates."""
        self.register(ValidationGate(Phase.VALIDATION, Phase.IDEATION))
        self.register(IdeationGate(Phase.IDEATION, Phase.PRODUCTION))
        self.register(ProductionGate(Phase.PRODUCTION, Phase.EXECUTION))
        self.register(ExecutionGate(Phase.EXECUTION, Phase.RENTABILISATION))
        self.register(RentabilisationGate(Phase.RENTABILISATION, Phase.ITERATION))
        self.register(IterationGate(Phase.ITERATION, Phase.ITERATION))

    def register(self, gate: QualityGate) -> None:
        """Register a quality gate."""
        key = (gate.from_phase, gate.to_phase)
        self._gates[key] = gate

    def get_gate(self, from_phase: Phase, to_phase: Phase) -> Optional[QualityGate]:
        """Get gate for a specific transition."""
        return self._gates.get((from_phase, to_phase))

    def can_transition(
        self, project: Project, to_phase: Phase
    ) -> tuple[bool, Optional[GateResult]]:
        """Check if project can transition to target phase."""
        gate = self.get_gate(project.phase, to_phase)

        if gate is None:
            # No gate defined - allow transition
            return True, None

        result = gate.evaluate(project)
        return result.can_transition, result

    def validate_transition(self, project: Project, to_phase: Phase) -> GateResult:
        """Validate transition and return detailed result."""
        gate = self.get_gate(project.phase, to_phase)

        if gate is None:
            # Create a default passing result
            return GateResult(
                gate_name="Default Gate",
                from_phase=project.phase,
                to_phase=to_phase,
                status=GateStatus.PASSED,
                score=10.0,
                criteria_results=[],
                recommendations=[],
                blocking_issues=[],
            )

        return gate.evaluate(project)

    def list_gates(self) -> List[Dict[str, Any]]:
        """List all registered gates."""
        return [
            {
                "name": gate.name,
                "from_phase": gate.from_phase.value,
                "to_phase": gate.to_phase.value,
                "criteria_count": len(gate.criteria),
                "minimum_score": gate.minimum_score,
            }
            for gate in self._gates.values()
        ]


# Global registry instance
gate_registry = QualityGateRegistry()


def check_transition(project: Project, to_phase: Phase) -> tuple[bool, Optional[GateResult]]:
    """Convenience function to check if transition is allowed."""
    return gate_registry.can_transition(project, to_phase)


def validate_transition(project: Project, to_phase: Phase) -> GateResult:
    """Convenience function to validate transition."""
    return gate_registry.validate_transition(project, to_phase)
