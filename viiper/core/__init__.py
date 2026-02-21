"""Core module initialization."""

from viiper.core.phase import Phase
from viiper.core.variant import Variant
from viiper.core.project import Project
from viiper.core.health import HealthScore, HealthDimension
from viiper.core.quality_gates import (
    QualityGate,
    ValidationGate,
    IdeationGate,
    ProductionGate,
    ExecutionGate,
    RentabilisationGate,
    IterationGate,
    QualityGateRegistry,
    GateResult,
    GateStatus,
    check_transition,
    validate_transition,
    gate_registry,
)

__all__ = [
    "Phase",
    "Variant",
    "Project",
    "HealthScore",
    "HealthDimension",
    "QualityGate",
    "ValidationGate",
    "IdeationGate",
    "ProductionGate",
    "ExecutionGate",
    "RentabilisationGate",
    "IterationGate",
    "QualityGateRegistry",
    "GateResult",
    "GateStatus",
    "check_transition",
    "validate_transition",
    "gate_registry",
]
