"""
Phase management for VIIPER methodology.

Defines the 6 phases of VIIPER: V → I → P → E → R → I²
"""

from enum import Enum
from typing import Optional


class Phase(str, Enum):
    """
    The six phases of VIIPER methodology.
    
    Each phase has specific goals, deliverables, and success criteria.
    """
    
    VALIDATION = "validation"  # V: Market validation, problem-solution fit
    IDEATION = "ideation"      # I: Architecture, design, planning
    PRODUCTION = "production"  # P: Development, testing, deployment
    EXECUTION = "execution"    # E: Launch, user acquisition, marketing
    RENTABILISATION = "rentabilisation"  # R: Monetization, optimization
    ITERATION = "iteration"    # I²: Continuous improvement, feature dev
    
    def __str__(self) -> str:
        return self.value
    
    @property
    def display_name(self) -> str:
        """Get human-readable display name."""
        return self.value.capitalize()
    
    @property
    def short_code(self) -> str:
        """Get single-letter code."""
        codes = {
            Phase.VALIDATION: "V",
            Phase.IDEATION: "I",
            Phase.PRODUCTION: "P",
            Phase.EXECUTION: "E",
            Phase.RENTABILISATION: "R",
            Phase.ITERATION: "I²"
        }
        return codes[self]
    
    def next_phase(self) -> Optional["Phase"]:
        """Get the next phase in the sequence."""
        sequence = [
            Phase.VALIDATION,
            Phase.IDEATION,
            Phase.PRODUCTION,
            Phase.EXECUTION,
            Phase.RENTABILISATION,
            Phase.ITERATION
        ]
        
        try:
            current_index = sequence.index(self)
            if current_index < len(sequence) - 1:
                return sequence[current_index + 1]
            return None  # Already in final phase
        except ValueError:
            return None
    
    def previous_phase(self) -> Optional["Phase"]:
        """Get the previous phase in the sequence."""
        sequence = [
            Phase.VALIDATION,
            Phase.IDEATION,
            Phase.PRODUCTION,
            Phase.EXECUTION,
            Phase.RENTABILISATION,
            Phase.ITERATION
        ]
        
        try:
            current_index = sequence.index(self)
            if current_index > 0:
                return sequence[current_index - 1]
            return None  # Already in first phase
        except ValueError:
            return None
    
    @property
    def typical_duration_weeks(self) -> tuple[int, int]:
        """Get typical duration range in weeks (min, max)."""
        durations = {
            Phase.VALIDATION: (2, 4),
            Phase.IDEATION: (1, 3),
            Phase.PRODUCTION: (4, 12),
            Phase.EXECUTION: (2, 8),
            Phase.RENTABILISATION: (4, 12),
            Phase.ITERATION: (0, 0)  # Ongoing
        }
        return durations[self]
    
    @property
    def description(self) -> str:
        """Get phase description."""
        descriptions = {
            Phase.VALIDATION: "Market research, problem validation, willingness-to-pay testing",
            Phase.IDEATION: "Architecture design, tech stack selection, planning",
            Phase.PRODUCTION: "Development, testing, security hardening",
            Phase.EXECUTION: "Launch, user acquisition, marketing campaigns",
            Phase.RENTABILISATION: "Monetization optimization, growth, retention",
            Phase.ITERATION: "Continuous improvement, feature development, scaling"
        }
        return descriptions[self]
