from abc import ABC, abstractmethod
from loguru import logger


class BaseMasker(ABC):
    """
    L - Liskov Substitution: both masker implementations are interchangeable.
    D - Dependency Inversion: consumers depend on this abstraction.
    """

    @abstractmethod
    def mask(self, text: str) -> str:
        pass


class DistilBertMasker(BaseMasker):
    """S - Single responsibility: mask PII using DistilBERT model only."""

    def mask(self, text: str) -> str:
        from Guardial import InputGuardial
        logger.info("[DistilBertMasker] Masking text using DistilBERT")
        return InputGuardial(text).result_data


class GlinerMasker(BaseMasker):
    """S - Single responsibility: mask PII using GLiNER model only."""

    def mask(self, text: str) -> str:
        from GlinerGuardial import GLiNERGuardial
        logger.info("[GlinerMasker] Masking text using GLiNER")
        return GLiNERGuardial(text).result_data


class MaskingService:
    """
    S - Single responsibility: resolve and apply the correct masker.
    O - Open/Closed: add new maskers without changing this class.
    """

    _maskers: dict[str, BaseMasker] = {
        "gliner": GlinerMasker(),
        "default": DistilBertMasker(),
    }

    def apply(self, text: str, strategy: str = "default") -> str:
        masker = self._maskers.get(strategy, self._maskers["default"])
        logger.info(f"[MaskingService] Applying masking strategy: '{strategy}'")
        return masker.mask(text)
