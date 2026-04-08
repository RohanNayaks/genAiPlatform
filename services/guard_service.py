import re
from abc import ABC, abstractmethod
from loguru import logger


class BaseGuard(ABC):
    """D - High-level modules depend on this abstraction, not concrete guard implementations."""

    @abstractmethod
    def is_jailbreak(self, text: str) -> bool:
        pass


class JailbreakGuardService(BaseGuard):
    """S - Single responsibility: detect and block jailbreak attempts only."""

    def __init__(self):
        logger.info("[JailbreakGuardService] Initializing")
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
        self.injection_patterns = [
            r"system\s*:\s*you",
            r"<\s*system\s*>",
            r"\[system\]",
            r"###\s*instruction",
            r"---\s*new\s*prompt",
            r"ignore\s+.{0,30}(above|prior|previous|preceding)",
            r"prompt\s*injection",
        ]
        logger.info(f"[JailbreakGuardService] Initialized with {len(self.banned_keywords)} keywords and {len(self.injection_patterns)} patterns")

    def is_jailbreak(self, text: str) -> bool:
        lower_text = text.lower()

        for keyword in self.banned_keywords:
            if keyword in lower_text:
                logger.warning(f"[JailbreakGuardService] Banned keyword detected: '{keyword}'")
                return True

        for pattern in self.injection_patterns:
            if re.search(pattern, lower_text):
                logger.warning(f"[JailbreakGuardService] Injection pattern matched: '{pattern}'")
                return True

        logger.info("[JailbreakGuardService] No jailbreak detected")
        return False
