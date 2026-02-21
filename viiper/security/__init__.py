"""
VIIPER Security Module.

Provides security layers for agents, especially those with internet access.
Protects against prompt injection, XSS, and malicious content.
"""

from viiper.security.prompt_injection import (
    PromptInjectionGuard,
    sanitize_input,
    sanitize_url,
    validate_search_query,
    SecurityLevel,
)
from viiper.security.content_filter import (
    ContentFilter,
    filter_sensitive_data,
    ContentSafetyResult,
)

__all__ = [
    # Prompt Injection Protection
    "PromptInjectionGuard",
    "sanitize_input",
    "sanitize_url",
    "validate_search_query",
    "SecurityLevel",
    # Content Filtering
    "ContentFilter",
    "filter_sensitive_data",
    "ContentSafetyResult",
]