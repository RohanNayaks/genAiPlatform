import re
from loguru import logger


class JailbreakGuard:
    """
    Detects and blocks potential jailbreak attempts using keyword and pattern matching.
    Provides an early-exit guard for malicious inputs before reaching the cache layer.
    """

    def __init__(self):
        logger.info("[JailbreakGuard] Initializing jailbreak guard")

        # Plain banned keywords (case-insensitive substring match)
        self.banned_keywords = [
            "ignore previous instructions",
            "ignore all instructions",
            "disregard your",
            "forget your instructions",
            "you are now",
            "act as",
            "pretend you are",
            "pretend to be",
            "roleplay as",
            "jailbreak",
            "bypass",
            "override instructions",
            "do anything now",
            "dan mode",
            "evil mode",
            "unrestricted mode",
        ]

        # Regex patterns for structural injection attacks
        self.injection_patterns = [
            r"system\s*:\s*you",           # system: you are ...
            r"<\s*system\s*>",             # <system> tags
            r"\[system\]",                 # [system] markers
            r"###\s*instruction",          # ### Instruction: ...
            r"---\s*new\s*prompt",         # --- new prompt ---
            r"ignore\s+.{0,30}(above|prior|previous|preceding)",  # ignore X instructions
            r"prompt\s*injection",
        ]

        logger.info(
            f"[JailbreakGuard] Initialized with {len(self.banned_keywords)} banned keywords "
            f"and {len(self.injection_patterns)} injection patterns"
        )

    def is_jailbreak(self, text: str) -> bool:
        """
        Checks if input text contains jailbreak attempts via keywords or patterns.

        Args:
            text: User input to check

        Returns:
            True if jailbreak detected, False otherwise
        """
        logger.info(f"[JailbreakGuard.is_jailbreak] Checking text for jailbreak: {text}")
        lower_text = text.lower()

        # Check banned keywords
        for keyword in self.banned_keywords:
            if keyword in lower_text:
                logger.warning(
                    f"[JailbreakGuard.is_jailbreak] Banned keyword detected: '{keyword}'"
                )
                return True

        # Check injection patterns
        for pattern in self.injection_patterns:
            if re.search(pattern, lower_text):
                logger.warning(
                    f"[JailbreakGuard.is_jailbreak] Injection pattern matched: '{pattern}'"
                )
                return True

        logger.info("[JailbreakGuard.is_jailbreak] No jailbreak detected")
        return False
