from langchain_core.prompts import PromptTemplate
from loguru import logger
from services.masking_service import MaskingService


class TemplateService:
    """S - Single responsibility: build the prompt template, delegating masking to MaskingService."""

    def __init__(self, masking_service: MaskingService):
        self.masking_service = masking_service

    def build(self, text: str, is_masking: bool = False, masking_strategy: str = "default") -> str:
        logger.info(f"[TemplateService] Building template, is_masking={is_masking}")

        utterance = (
            self.masking_service.apply(text, masking_strategy)
            if is_masking
            else text
        )

        prompt = PromptTemplate.from_template(
            "Generate utterance for the Intent: {adjective} here are few examples {content}."
        ).format(adjective=utterance, content=utterance)

        logger.info(f"[TemplateService] Template built: {prompt}")
        return prompt
