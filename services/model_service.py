from abc import ABC, abstractmethod
from loguru import logger


class BaseModelProvider(ABC):
    """
    I - Interface Segregation: every model only needs to implement generate().
    D - Dependency Inversion: consumers depend on this abstraction.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


class Phi3Provider(BaseModelProvider):
    """S - Single responsibility: invoke Phi3 model only."""

    def generate(self, prompt: str) -> str:
        logger.info("[Phi3Provider] Generating response")
        return f"Phi3 model response for {prompt}"


class OpenAIProvider(BaseModelProvider):
    """S - Single responsibility: invoke OpenAI model only."""

    def generate(self, prompt: str) -> str:
        logger.info("[OpenAIProvider] Generating response")
        return f"OpenAI model response for {prompt}"


class ClaudeProvider(BaseModelProvider):
    """S - Single responsibility: invoke Claude model only."""

    def generate(self, prompt: str) -> str:
        logger.info("[ClaudeProvider] Generating response")
        return f"Claude model response for {prompt}"


class GeminiProvider(BaseModelProvider):
    """S - Single responsibility: invoke Gemini model only."""

    def generate(self, prompt: str) -> str:
        logger.info("[GeminiProvider] Generating response")
        return f"Gemini model response for {prompt}"


class ModelService:
    """
    O - Open/Closed: register new providers without modifying this class.
    S - Single responsibility: route to the correct provider only.
    """

    _providers: dict[str, BaseModelProvider] = {
        "phi3": Phi3Provider(),
        "openai": OpenAIProvider(),
        "claude": ClaudeProvider(),
        "gemini": GeminiProvider(),
    }

    def generate(self, model_name: str, prompt: str) -> str:
        provider = self._providers.get(model_name.lower())

        if provider is None:
            logger.error(f"[ModelService] Unknown model: '{model_name}'")
            raise ValueError(f"Unsupported model: '{model_name}'")

        logger.info(f"[ModelService] Routing to provider: '{model_name}'")
        return provider.generate(prompt)
