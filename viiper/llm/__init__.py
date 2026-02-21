"""
VIIPER LLM Integration Module.

Provides access to multiple LLM providers for agents:
- NVIDIA: GLM5, Llama 405B, Llama 70B, Mixtral
- Kimi: K2.5 (long context, thinking)
"""

from viiper.llm.nvidia_llm import NvidiaLLM
from viiper.llm.unified_llm import (
    UnifiedLLM,
    LLMResponse,
    LLMProvider,
    ModelType,
    ModelCapabilities,
    MODEL_CONFIGS,
    get_llm,
    complete,
    chat,
)

__all__ = [
    # Unified interface (recommended)
    "UnifiedLLM",
    "LLMResponse",
    "LLMProvider",
    "ModelType",
    "ModelCapabilities",
    "MODEL_CONFIGS",
    "get_llm",
    "complete",
    "chat",
    # Legacy
    "NvidiaLLM",
]
