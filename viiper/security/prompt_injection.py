"""
Prompt Injection Protection for VIIPER Agents.

Protects agents from malicious prompts and inputs, especially for
agents with internet access (Browser, Search, etc.).

Security layers:
1. Input sanitization
2. Pattern detection
3. Context boundary enforcement
4. Output validation
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
from urllib.parse import urlparse, unquote
import html


class SecurityLevel(str, Enum):
    """Security threat levels."""
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SecurityScanResult:
    """Result of security scan."""
    is_safe: bool
    level: SecurityLevel
    threats_detected: List[str]
    sanitized_input: str
    original_input: str
    blocked_patterns: List[str]


class PromptInjectionGuard:
    """
    Guard against prompt injection attacks.
    
    Protects agents from:
    - System prompt extraction attempts
    - Role manipulation
    - Instruction override
    - Context boundary breaches
    - Malicious content injection
    
    Usage:
        guard = PromptInjectionGuard()
        result = guard.scan(user_input)
        if not result.is_safe:
            raise SecurityError(f"Blocked: {result.threats_detected}")
    """
    
    # Patterns that indicate potential prompt injection
    INJECTION_PATTERNS = [
        # System prompt extraction
        r"ignore\s+(all\s+)?(previous|above|prior)\s+(instructions|prompts|rules)",
        r"forget\s+(all\s+)?(previous|above|prior)\s+(instructions|prompts)",
        r"disregard\s+(all\s+)?(previous|above|prior)\s+(instructions|rules)",
        r"show\s+(me\s+)?(your|the)\s+(system\s+)?prompt",
        r"print\s+(your|the)\s+(system\s+)?prompt",
        r"repeat\s+(your|the)\s+(system\s+)?prompt",
        r"output\s+(your|the)\s+(system\s+)?prompt",
        r"what\s+(is|are)\s+(your|the)\s+(system\s+)?prompt",
        r"reveal\s+(your|the)\s+(system\s+)?prompt",
        
        # Role manipulation
        r"you\s+are\s+now\s+(a|an)\s+\w+",
        r"act\s+as\s+(if\s+you\s+are\s+)?(a|an)\s+\w+",
        r"pretend\s+(to\s+be|you\s+are)\s+(a|an)\s+\w+",
        r"role[- ]?play\s+as\s+(a|an)\s+\w+",
        r"simulate\s+(being\s+)?(a|an)\s+\w+",
        r"from\s+now\s+on\s+you\s+are",
        r"your\s+new\s+role\s+is",
        
        # Instruction override
        r"new\s+instructions?\s*:",
        r"override\s+(all\s+)?(previous\s+)?instructions",
        r"change\s+(your|the)\s+instructions",
        r"replace\s+(your|the)\s+instructions",
        r"update\s+(your|the)\s+instructions",
        r"modified\s+instructions?\s*:",
        
        # Context boundary breach
        r"\[system\]",
        r"\[assistant\]",
        r"\[user\]",
        r"\[admin\]",
        r"\[developer\]",
        r"<\|system\|>",
        r"<\|assistant\|>",
        r"<\|user\|>",
        r"<\|im_start\|>",
        r"<\|im_end\|>",
        r"<system>",
        r"</system>",
        r"###\s*system",
        r"###\s*assistant",
        
        # Escape attempts
        r"escape\s+(all\s+)?restrictions?",
        r"bypass\s+(all\s+)?(security|restrictions|filters)",
        r"disable\s+(all\s+)?(security|filters|restrictions)",
        r"jailbreak",
        r"do\s+anything\s+now",
        r"DAN\s+mode",
        
        # Code/script injection
        r"<script[^>]*>",
        r"javascript\s*:",
        r"on(error|load|click|mouse)\s*=",
        r"eval\s*\(",
        r"document\.(cookie|location|write)",
        r"window\.(location|open)",
        
        # SQL injection patterns (for web scraping)
        r"('\s*(or|and)\s*'|\"\s*(or|and)\s*\")",
        r"(union\s+(all\s+)?select)",
        r"(;\s*drop\s+table)",
        r"(;\s*delete\s+from)",
        r"(;\s*insert\s+into)",
        r"(;\s*update\s+\w+\s+set)",
        
        # Command injection
        r";\s*(rm|del|format|shutdown|reboot)",
        r"\|\s*(rm|del|cat|type)",
        r"`[^`]*`",
        r"\$\([^)]*\)",
        r"&&\s*(rm|del|cat)",
    ]
    
    # Compromised patterns for web content
    WEB_CONTENT_PATTERNS = [
        r"data\s*:\s*text/html",
        r"vbscript\s*:",
        r"@import\s+url",
        r"expression\s*\(",
        r"-moz-binding\s*:",
        r"behavior\s*:\s*url",
    ]
    
    # Maximum allowed lengths
    MAX_INPUT_LENGTH = 50000  # 50KB
    MAX_URL_LENGTH = 2048
    MAX_QUERY_LENGTH = 1000
    
    def __init__(
        self,
        strict_mode: bool = True,
        log_threats: bool = True,
    ):
        """
        Initialize the guard.
        
        Args:
            strict_mode: Block on any detected threat
            log_threats: Log detected threats for analysis
        """
        self.strict_mode = strict_mode
        self.log_threats = log_threats
        self._threat_log: List[Dict[str, Any]] = []
        
        # Compile patterns for efficiency
        self._compiled_patterns = [
            re.compile(pattern, re.IGNORECASE | re.MULTILINE)
            for pattern in self.INJECTION_PATTERNS
        ]
        self._compiled_web_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in self.WEB_CONTENT_PATTERNS
        ]
    
    def scan(self, input_text: str, context: str = "general") -> SecurityScanResult:
        """
        Scan input for potential threats.
        
        Args:
            input_text: Text to scan
            context: Context type (general, web, code, url)
        
        Returns:
            SecurityScanResult with safety assessment
        """
        original_input = input_text
        threats_detected = []
        blocked_patterns = []
        level = SecurityLevel.SAFE
        
        # Check length limits
        if len(input_text) > self.MAX_INPUT_LENGTH:
            threats_detected.append("Input exceeds maximum length")
            level = SecurityLevel.HIGH
            input_text = input_text[:self.MAX_INPUT_LENGTH]
        
        # Scan for injection patterns
        for i, pattern in enumerate(self._compiled_patterns):
            matches = pattern.findall(input_text)
            if matches:
                pattern_name = self.INJECTION_PATTERNS[i][:50]
                threats_detected.append(f"Injection pattern detected: {pattern_name}")
                blocked_patterns.extend(matches)
                level = self._escalate_level(level, SecurityLevel.HIGH)
        
        # Additional web content scanning
        if context in ["web", "url", "search"]:
            for i, pattern in enumerate(self._compiled_web_patterns):
                matches = pattern.findall(input_text)
                if matches:
                    threats_detected.append(f"Malicious web pattern detected")
                    blocked_patterns.extend(matches)
                    level = self._escalate_level(level, SecurityLevel.CRITICAL)
        
        # Sanitize input
        sanitized_input = self._sanitize(input_text)
        
        # Determine if safe
        is_safe = level in [SecurityLevel.SAFE, SecurityLevel.LOW]
        
        # Log threat if detected
        if threats_detected and self.log_threats:
            self._log_threat(original_input, threats_detected, level)
        
        return SecurityScanResult(
            is_safe=is_safe,
            level=level,
            threats_detected=threats_detected,
            sanitized_input=sanitized_input,
            original_input=original_input,
            blocked_patterns=blocked_patterns[:10],  # Limit for memory
        )
    
    def scan_url(self, url: str) -> SecurityScanResult:
        """
        Scan URL for safety.
        
        Args:
            url: URL to scan
        
        Returns:
            SecurityScanResult
        """
        threats = []
        level = SecurityLevel.SAFE
        
        # Check length
        if len(url) > self.MAX_URL_LENGTH:
            threats.append("URL exceeds maximum length")
            level = SecurityLevel.HIGH
            url = url[:self.MAX_URL_LENGTH]
        
        # Parse and validate URL
        try:
            parsed = urlparse(url)
            
            # Check for dangerous schemes
            dangerous_schemes = ["javascript", "vbscript", "data", "file"]
            if parsed.scheme.lower() in dangerous_schemes:
                threats.append(f"Dangerous URL scheme: {parsed.scheme}")
                level = SecurityLevel.CRITICAL
            
            # Check for encoded injection attempts
            decoded = unquote(url)
            for pattern in self._compiled_patterns:
                if pattern.search(decoded):
                    threats.append("Encoded injection attempt in URL")
                    level = SecurityLevel.CRITICAL
                    break
            
            # Check for suspicious domains
            suspicious_tlds = [".xyz", ".top", ".click", ".link", ".work"]
            if any(parsed.netloc.endswith(tld) for tld in suspicious_tlds):
                if level == SecurityLevel.SAFE:
                    level = SecurityLevel.LOW
                    threats.append("Suspicious TLD")
            
        except Exception as e:
            threats.append(f"Invalid URL format: {str(e)}")
            level = SecurityLevel.MEDIUM
        
        return SecurityScanResult(
            is_safe=level in [SecurityLevel.SAFE, SecurityLevel.LOW],
            level=level,
            threats_detected=threats,
            sanitized_input=url,
            original_input=url,
            blocked_patterns=[],
        )
    
    def _sanitize(self, text: str) -> str:
        """Sanitize input text."""
        # HTML escape
        text = html.escape(text)
        
        # Remove null bytes
        text = text.replace("\x00", "")
        
        # Normalize whitespace
        text = re.sub(r"\s+", " ", text)
        
        return text.strip()
    
    def _escalate_level(self, current: SecurityLevel, new: SecurityLevel) -> SecurityLevel:
        """Escalate to higher threat level."""
        levels = [SecurityLevel.SAFE, SecurityLevel.LOW, SecurityLevel.MEDIUM, 
                  SecurityLevel.HIGH, SecurityLevel.CRITICAL]
        current_idx = levels.index(current)
        new_idx = levels.index(new)
        return levels[max(current_idx, new_idx)]
    
    def _log_threat(self, input_text: str, threats: List[str], level: SecurityLevel):
        """Log detected threat for analysis."""
        self._threat_log.append({
            "timestamp": __import__("datetime").datetime.now().isoformat(),
            "level": level.value,
            "threats": threats,
            "input_preview": input_text[:200],
        })
    
    def get_threat_log(self) -> List[Dict[str, Any]]:
        """Get logged threats."""
        return self._threat_log.copy()
    
    def clear_log(self) -> None:
        """Clear threat log."""
        self._threat_log.clear()


# Convenience functions

def sanitize_input(text: str, strict: bool = True) -> str:
    """
    Sanitize user input.
    
    Args:
        text: Input to sanitize
        strict: Raise exception on threat if True
    
    Returns:
        Sanitized text
    
    Raises:
        ValueError: If threat detected in strict mode
    """
    guard = PromptInjectionGuard(strict_mode=strict)
    result = guard.scan(text)
    
    if not result.is_safe and strict:
        raise ValueError(f"Potential security threat: {result.threats_detected[0]}")
    
    return result.sanitized_input


def sanitize_url(url: str, strict: bool = True) -> str:
    """
    Sanitize URL.
    
    Args:
        url: URL to sanitize
        strict: Raise exception on threat if True
    
    Returns:
        Sanitized URL
    
    Raises:
        ValueError: If threat detected in strict mode
    """
    guard = PromptInjectionGuard(strict_mode=strict)
    result = guard.scan_url(url)
    
    if not result.is_safe and strict:
        raise ValueError(f"Unsafe URL: {result.threats_detected[0]}")
    
    return result.sanitized_input


def validate_search_query(query: str, max_length: int = 500) -> str:
    """
    Validate and sanitize a search query.
    
    Args:
        query: Search query
        max_length: Maximum allowed length
    
    Returns:
        Sanitized query
    
    Raises:
        ValueError: If query is invalid or dangerous
    """
    if not query or not query.strip():
        raise ValueError("Empty search query")
    
    if len(query) > max_length:
        query = query[:max_length]
    
    guard = PromptInjectionGuard()
    result = guard.scan(query, context="search")
    
    if not result.is_safe:
        raise ValueError(f"Invalid search query: potential injection detected")
    
    # Additional query-specific sanitization
    query = result.sanitized_input
    
    # Remove special characters that might break searches
    query = re.sub(r"[{}()\[\]\\^~*!?:;]", " ", query)
    query = re.sub(r"\s+", " ", query).strip()
    
    return query