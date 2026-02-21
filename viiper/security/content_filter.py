"""
Content Filter for VIIPER Agents.

Filters and validates content from external sources (web, APIs, etc.)
to prevent malicious data from affecting agent behavior.
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json


class ContentType(str, Enum):
    """Types of content to filter."""
    TEXT = "text"
    HTML = "html"
    JSON = "json"
    URL = "url"
    CODE = "code"


@dataclass
class ContentSafetyResult:
    """Result of content safety check."""
    is_safe: bool
    content_type: ContentType
    filtered_content: str
    removed_elements: List[str]
    warnings: List[str]
    risk_score: float  # 0.0 = safe, 1.0 = dangerous


class ContentFilter:
    """
    Filter content from external sources.
    
    Features:
    - Remove malicious scripts
    - Filter PII (optional)
    - Detect phishing attempts
    - Validate JSON structure
    - Sanitize HTML content
    """
    
    # Patterns for malicious content
    MALICIOUS_PATTERNS = [
        # Scripts and code execution
        (r"<script[^>]*>.*?</script>", "script_tag"),
        (r"javascript\s*:", "javascript_protocol"),
        (r"vbscript\s*:", "vbscript_protocol"),
        (r"on\w+\s*=", "event_handler"),
        
        # Data exfiltration
        (r"document\.cookie", "cookie_access"),
        (r"document\.location", "location_access"),
        (r"window\.location", "window_location"),
        (r"XMLHttpRequest", "xhr_request"),
        (r"fetch\s*\(", "fetch_api"),
        
        # iframe injections
        (r"<iframe[^>]*>", "iframe_injection"),
        
        # Meta redirects
        (r"<meta[^>]*http-equiv\s*=\s*[\"']?refresh", "meta_redirect"),
        
        # Form hijacking
        (r"<form[^>]*action\s*=\s*[\"']?https?://(?!localhost)", "external_form"),
        
        # Obfuscated code
        (r"eval\s*\(", "eval_call"),
        (r"atob\s*\(", "base64_decode"),
        (r"String\.fromCharCode", "char_code_obfuscation"),
        
        # Phishing indicators
        (r"password\s*:", "password_field"),
        (r"credit\s*card", "cc_field"),
        (r"social\s*security", "ssn_field"),
    ]
    
    # PII patterns (optional filtering)
    PII_PATTERNS = [
        (r"\b\d{3}-\d{2}-\d{4}\b", "ssn"),
        (r"\b\d{16}\b", "credit_card"),
        (r"\b[\w\.-]+@[\w\.-]+\.\w+\b", "email"),
        (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "phone"),
        (r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", "ip_address"),
    ]
    
    # Maximum content sizes
    MAX_CONTENT_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_HTML_SIZE = 5 * 1024 * 1024  # 5MB
    MAX_JSON_SIZE = 1 * 1024 * 1024  # 1MB
    
    def __init__(
        self,
        filter_pii: bool = False,
        strict_mode: bool = True,
        preserve_structure: bool = True,
    ):
        """
        Initialize content filter.
        
        Args:
            filter_pii: Remove PII from content
            strict_mode: Reject content with any malicious patterns
            preserve_structure: Try to preserve valid structure when filtering
        """
        self.filter_pii = filter_pii
        self.strict_mode = strict_mode
        self.preserve_structure = preserve_structure
        
        # Compile patterns
        self._malicious = [
            (re.compile(p, re.IGNORECASE | re.DOTALL), name)
            for p, name in self.MALICIOUS_PATTERNS
        ]
        self._pii = [
            (re.compile(p, re.IGNORECASE), name)
            for p, name in self.PII_PATTERNS
        ]
    
    def filter(
        self,
        content: str,
        content_type: ContentType = ContentType.TEXT,
    ) -> ContentSafetyResult:
        """
        Filter content for safety.
        
        Args:
            content: Content to filter
            content_type: Type of content
        
        Returns:
            ContentSafetyResult with filtered content
        """
        removed_elements = []
        warnings = []
        risk_score = 0.0
        
        # Check size limits
        if len(content) > self.MAX_CONTENT_SIZE:
            warnings.append(f"Content exceeds max size, truncated")
            content = content[:self.MAX_CONTENT_SIZE]
            risk_score = max(risk_score, 0.1)
        
        # Check for malicious patterns
        filtered_content = content
        for pattern, name in self._malicious:
            matches = pattern.findall(filtered_content)
            if matches:
                removed_elements.append(f"{name}: {len(matches)} occurrence(s)")
                risk_score = max(risk_score, 0.8)
                
                if self.preserve_structure and content_type == ContentType.HTML:
                    # Replace with safe placeholder
                    filtered_content = pattern.sub("<!-- filtered -->", filtered_content)
                else:
                    filtered_content = pattern.sub("", filtered_content)
        
        # Optional PII filtering
        if self.filter_pii:
            for pattern, name in self._pii:
                matches = pattern.findall(filtered_content)
                if matches:
                    removed_elements.append(f"pii_{name}: {len(matches)} occurrence(s)")
                    filtered_content = pattern.sub("[REDACTED]", filtered_content)
        
        # Content-type specific validation
        if content_type == ContentType.JSON:
            filtered_content, json_warnings = self._validate_json(filtered_content)
            warnings.extend(json_warnings)
        elif content_type == ContentType.HTML:
            filtered_content, html_warnings = self._validate_html(filtered_content)
            warnings.extend(html_warnings)
        elif content_type == ContentType.URL:
            url_warning = self._validate_url_content(filtered_content)
            if url_warning:
                warnings.append(url_warning)
        
        # Determine safety
        is_safe = risk_score < 0.5 if self.strict_mode else risk_score < 0.8
        
        return ContentSafetyResult(
            is_safe=is_safe,
            content_type=content_type,
            filtered_content=filtered_content,
            removed_elements=removed_elements,
            warnings=warnings,
            risk_score=risk_score,
        )
    
    def filter_html(self, html_content: str) -> ContentSafetyResult:
        """Filter HTML content specifically."""
        return self.filter(html_content, ContentType.HTML)
    
    def filter_json(self, json_content: str) -> ContentSafetyResult:
        """Filter JSON content specifically."""
        return self.filter(json_content, ContentType.JSON)
    
    def _validate_json(self, content: str) -> tuple:
        """Validate JSON structure."""
        warnings = []
        try:
            parsed = json.loads(content)
            # Check for suspicious keys
            suspicious_keys = ["password", "secret", "token", "api_key", "credential"]
            def check_dict(d):
                if isinstance(d, dict):
                    for key in d.keys():
                        if any(s in str(key).lower() for s in suspicious_keys):
                            warnings.append(f"Suspicious key found: {key}")
                    for v in d.values():
                        check_dict(v)
                elif isinstance(d, list):
                    for item in d:
                        check_dict(item)
            check_dict(parsed)
            return content, warnings
        except json.JSONDecodeError as e:
            warnings.append(f"Invalid JSON: {str(e)}")
            return content, warnings
    
    def _validate_html(self, content: str) -> tuple:
        """Validate HTML content."""
        warnings = []
        
        # Check for unclosed tags (basic validation)
        open_tags = re.findall(r"<(\w+)[^>]*>", content)
        close_tags = re.findall(r"</(\w+)>", content)
        
        # Count self-closing tags
        self_closing = ["br", "hr", "img", "input", "meta", "link", "area", "base", "col", "embed", "param", "source", "track", "wbr"]
        
        open_count = {}
        for tag in open_tags:
            if tag.lower() not in self_closing:
                open_count[tag] = open_count.get(tag, 0) + 1
        
        for tag in close_tags:
            if tag in open_count:
                open_count[tag] -= 1
        
        for tag, count in open_count.items():
            if count > 0:
                warnings.append(f"Unclosed <{tag}> tag detected")
        
        return content, warnings
    
    def _validate_url_content(self, content: str) -> Optional[str]:
        """Validate URL-like content."""
        # Check for URL injection patterns
        url_patterns = [
            r"@.*?:",  # Basic auth in URL
            r"\\.\\.",  # Directory traversal
            r"%00",  # Null byte
        ]
        
        for pattern in url_patterns:
            if re.search(pattern, content):
                return f"Potential URL injection detected"
        
        return None
    
    def extract_safe_text(self, html_content: str) -> str:
        """
        Extract safe text from HTML content.
        
        Args:
            html_content: HTML to extract text from
        
        Returns:
            Plain text with HTML tags removed
        """
        # Remove script and style tags first
        text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html_content, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove all other tags
        text = re.sub(r"<[^>]+>", " ", text)
        
        # Decode HTML entities
        import html
        text = html.unescape(text)
        
        # Normalize whitespace
        text = re.sub(r"\s+", " ", text)
        
        return text.strip()


def filter_sensitive_data(content: str, content_type: str = "text") -> str:
    """
    Quick filter function for sensitive data.
    
    Args:
        content: Content to filter
        content_type: Type of content (text, html, json)
    
    Returns:
        Filtered content
    """
    ct_map = {
        "text": ContentType.TEXT,
        "html": ContentType.HTML,
        "json": ContentType.JSON,
        "url": ContentType.URL,
        "code": ContentType.CODE,
    }
    
    filter_instance = ContentFilter(filter_pii=True)
    result = filter_instance.filter(content, ct_map.get(content_type, ContentType.TEXT))
    
    return result.filtered_content