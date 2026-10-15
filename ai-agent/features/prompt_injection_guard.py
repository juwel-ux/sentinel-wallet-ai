"""
Prompt Injection Defense module.
Detects and blocks hidden instructions in external data.
"""

import re


INJECTION_PATTERNS = [
    r"ignore\s+(?:all\s+)?(?:previous\s+)?instructions",
    r"send\s+(?:all|everything)\s+(?:eth|money|funds)",
    r"transfer\s+(?:all|everything)",
    r"forward\s+(?:all|everything)",
    r"0x[a-fA-F0-9]{40}.*send",
    r"important:.*send",
    r"urgent:.*transfer",
    r"system:\s*",
    r"assistant:\s*",
    r"\[INST\]",
    r"<\|im_start\|>",
]


class PromptInjectionGuard:
    def __init__(self):
        self.blocked_count = 0
    
    def scan(self, text):
        """Scan text for injection attempts."""
        if not text:
            return True, "OK"
        
        text_lower = text.lower()
        
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, text_lower):
                self.blocked_count += 1
                return False, f"INJECTION_DETECTED: pattern '{pattern}'"
        
        return True, "OK"
    
    def sanitize(self, text):
        """Remove suspicious content."""
        if not text:
            return text
        
        for pattern in INJECTION_PATTERNS:
            text = re.sub(pattern, "[REDACTED]", text, flags=re.IGNORECASE)
        
        return text


_guard = None


def get_guard():
    global _guard
    if _guard is None:
        _guard = PromptInjectionGuard()
    return _guard


def scan_for_injection(text):
    guard = get_guard()
    return guard.scan(text)


def sanitize_input(text):
    guard = get_guard()
    return guard.sanitize(text)
