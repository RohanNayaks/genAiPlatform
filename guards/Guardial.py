from transformers import pipeline
from loguru import logger
import warnings
warnings.filterwarnings('ignore')

class InputGuardial:

    def __init__(self,text):
        # Initiating all the parametrs required to genrate entity extraction
        logger.info(f"[InputGuardial] Initializing entity extraction for text: {text}")
        MODEL_TAG = "Isotonic/distilbert_finetuned_ai4privacy_v2" # model name
        DEVICE = -1 # Use CPU
        self.unmasked_text = text
        logger.info("[InputGuardial] Loading entity extraction model")
        self.model = pipeline("token-classification", model=MODEL_TAG, tokenizer=MODEL_TAG, device=DEVICE) # Inititaing Pipline
        logger.info("[InputGuardial] Model loaded, running inference")
        self.model_output = self.model(text, aggregation_strategy="simple") # Genrating model output
        logger.info(f"[InputGuardial] Model output: {self.model_output}")
        self.result_data = self.replace_entities(entity_map=self.create_entity_map(self.model_output, text),text=text) # Generating the masked data
        logger.info(f"[InputGuardial] Masked data result: {self.result_data}")

    def create_entity_map(self,model_output,text):
        # creatng and entity mapper and return the mapped object
        logger.info("[InputGuardial.create_entity_map] Creating entity map")
        entity_map = {}
        for token in model_output:
            start = token["start"]
            end = token["end"]
            entity = text[start: end]
            entity_map[entity] = token["entity_group"]
        logger.info(f"[InputGuardial.create_entity_map] Entity map created: {entity_map}")
        return entity_map

    def replace_entities(self,text,entity_map):
        #The method replaces the words with the entity mapped name ex:- [FirstName]
        logger.info("[InputGuardial.replace_entities] Replacing entities in text")
        for word in entity_map:
            if word in self.unmasked_text:
                text = text.replace(word, f"[{entity_map[word]}]")
        return text