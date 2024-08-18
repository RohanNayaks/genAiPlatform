from transformers import pipeline
import warnings
warnings.filterwarnings('ignore')

class InputGuardial:

    def __init__(self,text):
        MODEL_TAG = "Isotonic/distilbert_finetuned_ai4privacy_v2"
        DEVICE = -1
        self.unmasked_text = text
        self.model = pipeline("token-classification", model=MODEL_TAG, tokenizer=MODEL_TAG, device=DEVICE)
        self.model_output = self.model(text, aggregation_strategy="simple")
        self.result_data = self.replace_entities(entity_map=self.create_entity_map(self.model_output, text),text=text)
    
    def create_entity_map(self,model_output,text):
        entity_map = {}
        for token in model_output:
            start = token["start"]
            end = token["end"]
            entity = text[start: end]
            entity_map[entity] = token["entity_group"]
        return entity_map
    
    def replace_entities(self,text,entity_map):
        for word in entity_map:
            if word in self.unmasked_text:
                text = text.replace(word, f"[{entity_map[word]}]")
        return text