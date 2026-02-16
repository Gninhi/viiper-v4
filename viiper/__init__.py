"""
VIIPER V4: Revolutionary Multi-Agent Framework for Product Development

This package provides a complete framework for managing product development
using multi-agent orchestration, collective intelligence, and meta-learning.
"""

__version__ = "0.1.0"
__author__ = "VIIPER Team"

from viiper.core.phase import Phase
from viiper.core.variant import Variant
from viiper.core.project import Project
from viiper.core.health import HealthScore

__all__ = ["Phase", "Variant", "Project", "HealthScore"]
