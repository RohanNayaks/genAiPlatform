from gliner import GLiNER
from loguru import logger
import warnings

warnings.filterwarnings('ignore')


class GLiNERGuardial:
    """
    Enhanced entity masking using GLiNER (Generalist Named Entity Recognition).
    Provides zero-shot entity typing with customizable labels.
    Drop-in replacement for InputGuardial with the same interface.
    """

    # Default labels for entity detection - mirrors common PII categories
    DEFAULT_LABELS = [
        "person", "email", "phone number", "address",
        "organization", "date", "credit card", "ssn",
    ]

    def __init__(self, text: str):
        """
        Initializes GLiNERGuardial with entity extraction and masking.

        Args:
            text: Input text to mask
        """
        logger.info(f"[GLiNERGuardial] Initializing entity extraction for text: {text}")
        MODEL_TAG = "urchade/gliner_mediumv2.1"
        self.unmasked_text = text

        logger.info("[GLiNERGuardial] Loading GLiNER model")
        self.model = GLiNER.from_pretrained(MODEL_TAG)

        logger.info("[GLiNERGuardial] Model loaded, running inference")
        self.model_output = self.model.predict_entities(
            text, self.DEFAULT_LABELS, threshold=0.5
        )
        logger.info(f"[GLiNERGuardial] Model output: {self.model_output}")

        self.result_data = self.replace_entities(
            entity_map=self.create_entity_map(self.model_output, text),
            text=text
        )
        logger.info(f"[GLiNERGuardial] Masked data result: {self.result_data}")

    def create_entity_map(self, model_output: list, text: str) -> dict:
        """
        Creates a mapping of entities to their types from GLiNER model output.

        Args:
            model_output: List of entity dicts from GLiNER
            text: Original text (for reference)

        Returns:
            Dictionary mapping entity text to entity label
        """
        logger.info("[GLiNERGuardial.create_entity_map] Creating entity map")
        entity_map = {}
        for entity in model_output:
            # GLiNER uses 'text' and 'label' keys (vs HuggingFace 'start'/'end'/'entity_group')
            entity_text = entity["text"]
            entity_label = entity["label"].upper()
            entity_map[entity_text] = entity_label

        logger.info(f"[GLiNERGuardial.create_entity_map] Entity map created: {entity_map}")
        return entity_map

    def replace_entities(self, text: str, entity_map: dict) -> str:
        """
        Replaces detected entities with their masked labels.

        Args:
            text: Original text with entities
            entity_map: Dictionary of {entity: label}

        Returns:
            Text with entities replaced by [LABEL] format
        """
        logger.info("[GLiNERGuardial.replace_entities] Replacing entities in text")
        for word in entity_map:
            if word in self.unmasked_text:
                text = text.replace(word, f"[{entity_map[word]}]")
        return text
